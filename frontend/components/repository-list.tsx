"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  listRepositories,
  Repository,
} from "@/lib/api";

interface RepositoryListProps {
  refreshKey: number;
}

export function RepositoryList({
  refreshKey,
}: RepositoryListProps) {
  const router = useRouter();

  const [repositories, setRepositories] = useState<
    Repository[]
  >([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const data = await listRepositories();

        if (!cancelled) {
          setRepositories(data);
        }
      } catch (error) {
        if (!cancelled) {
          setError(
            error instanceof Error
              ? error.message
              : "Failed to load repositories",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  function openRepository(repositoryId: string) {
    router.push(
      `/repositories/${repositoryId}`,
    );
  }

  if (loading) {
    return (
      <section className="mt-8">
        <h2 className="mb-4 text-xl font-semibold">
          Repositories
        </h2>

        <p className="text-sm text-gray-500">
          Loading repositories...
        </p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="mt-8">
        <p
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700"
        >
          {error}
        </p>
      </section>
    );
  }

  if (repositories.length === 0) {
    return (
      <section className="mt-8">
        <p className="text-sm text-gray-500">
          No repositories added yet.
        </p>
      </section>
    );
  }

  return (
    <section className="mt-10">
      <h2 className="mb-4 text-xl font-semibold">
        Repositories
      </h2>

      <div className="space-y-3">
        {repositories.map((repository) => (
          <article
            key={repository.id}
            role="button"
            tabIndex={0}
            onClick={() =>
              openRepository(repository.id)
            }
            onKeyDown={(event) => {
              if (
                event.key === "Enter" ||
                event.key === " "
              ) {
                event.preventDefault();

                openRepository(repository.id);
              }
            }}
            className="cursor-pointer rounded-xl border border-gray-200 bg-white p-5 transition hover:border-gray-400 hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-400"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0">
                <h3 className="font-medium">
                  {repository.owner}/
                  {repository.name}
                </h3>

                <p className="mt-1 truncate text-sm text-gray-500">
                  {repository.github_url}
                </p>
              </div>

              <span className="shrink-0 rounded-full bg-gray-100 px-3 py-1 text-xs font-medium capitalize">
                {repository.status}
              </span>
            </div>

            <p className="mt-4 text-sm font-medium">
              Open repository →
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
