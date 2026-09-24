"use client";

import { useEffect, useState } from "react";

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
  const [repositories, setRepositories] = useState<
    Repository[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);

      try {
        const data = await listRepositories();
        setRepositories(data);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to load repositories",
        );
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [refreshKey]);

  if (loading) {
    return <p>Loading repositories...</p>;
  }

  if (error) {
    return <p role="alert">{error}</p>;
  }

  if (repositories.length === 0) {
    return <p>No repositories added yet.</p>;
  }

  return (
    <section className="mt-8">
      <h2 className="mb-4 text-xl font-semibold">
        Repositories
      </h2>

      <div className="space-y-3">
        {repositories.map((repository) => (
          <article
            key={repository.id}
            className="rounded-lg border p-4"
          >
            <h3 className="font-medium">
              {repository.owner}/{repository.name}
            </h3>

            <p className="text-sm">
              {repository.github_url}
            </p>

            <p className="mt-2 text-sm">
              Status: {repository.status}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}