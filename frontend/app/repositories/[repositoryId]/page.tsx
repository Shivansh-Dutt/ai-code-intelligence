"use client";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { useParams } from "next/navigation";

import {
  listRepositories,
  Repository,
} from "@/lib/api";

import { RepositoryIngestion } from "@/components/repository-ingestion";
import { RepositoryQA } from "@/components/repository-qa";

export default function RepositoryPage() {
  const params = useParams();

  const repositoryId =
    params.repositoryId as string;

  const [repository, setRepository] =
    useState<Repository | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [indexed, setIndexed] =
    useState(false);

  /*
   * Load repository.
   *
   * Currently we use listRepositories()
   * because the API layer does not yet have
   * GET /api/repositories/{id}.
   */
  useEffect(() => {
    let cancelled = false;

    async function loadRepository() {
      setLoading(true);
      setError(null);

      try {
        const repositories =
          await listRepositories();

        const found =
          repositories.find(
            (item) =>
              item.id === repositoryId,
          );

        if (!found) {
          throw new Error(
            "Repository not found",
          );
        }

        if (!cancelled) {
          setRepository(found);

          setIndexed(
            found.status === "completed",
          );
        }
      } catch (error) {
        if (!cancelled) {
          setError(
            error instanceof Error
              ? error.message
              : "Failed to load repository",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadRepository();

    return () => {
      cancelled = true;
    };
  }, [repositoryId]);

  /*
   * Called after ingestion completes.
   */
  const handleIngestionCompleted =
    useCallback(() => {
      setIndexed(true);

      setRepository(
        (current) =>
          current
            ? {
                ...current,
                status: "completed",
              }
            : current,
      );
    }, []);

  if (loading) {
    return (
      <main className="mx-auto min-h-screen max-w-5xl px-6 py-12">
        <p className="text-sm text-gray-500">
          Loading repository...
        </p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="mx-auto min-h-screen max-w-5xl px-6 py-12">
        <div className="rounded-xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
          {error}
        </div>
      </main>
    );
  }

  if (!repository) {
    return (
      <main className="mx-auto min-h-screen max-w-5xl px-6 py-12">
        <p>Repository not found.</p>
      </main>
    );
  }

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-6 py-12">
      {/* Repository header */}
      <header>
        <p className="text-sm text-gray-500">
          Repository
        </p>

        <h1 className="mt-1 text-3xl font-bold">
          {repository.owner}/
          {repository.name}
        </h1>

        <a
          href={repository.github_url}
          target="_blank"
          rel="noreferrer"
          className="mt-2 inline-block text-sm text-gray-500 underline underline-offset-4 hover:text-black"
        >
          {repository.github_url}
        </a>

        <div className="mt-4 flex flex-wrap gap-3 text-sm">
          <span className="rounded-full bg-gray-100 px-3 py-1 capitalize">
            Repository: {repository.status}
          </span>

          {repository.default_branch && (
            <span className="rounded-full bg-gray-100 px-3 py-1">
              Branch:{" "}
              {repository.default_branch}
            </span>
          )}

          {repository.commit_sha && (
            <span className="rounded-full bg-gray-100 px-3 py-1 font-mono">
              Commit:{" "}
              {repository.commit_sha.slice(
                0,
                7,
              )}
            </span>
          )}
        </div>
      </header>

      {/* Main content */}
      <div className="mt-10 space-y-8">
        <RepositoryIngestion
          repositoryId={repository.id}
          repositoryStatus={
            repository.status
          }
          onCompleted={
            handleIngestionCompleted
          }
        />

        {indexed ? (
          <RepositoryQA
            repositoryId={repository.id}
          />
        ) : (
          <section className="rounded-xl border border-dashed border-gray-300 bg-gray-50 p-8 text-center">
            <h2 className="text-lg font-semibold">
              Repository Q&A
            </h2>

            <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-gray-500">
              Index the repository first. Once
              the source files and embeddings are
              ready, you can ask questions about
              the codebase.
            </p >         </section>
        )}
      </div>
    </main>
  );
}
