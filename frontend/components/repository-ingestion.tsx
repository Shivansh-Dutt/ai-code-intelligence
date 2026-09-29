"use client";

import {
  useEffect,
  useState,
} from "react";

import {
  getIngestionJob,
  IngestionJob,
  IngestionStatus,
  startIngestion,
} from "@/lib/api";

interface RepositoryIngestionProps {
  repositoryId: string;
  repositoryStatus: string;
  onCompleted?: () => void;
}

function statusLabel(status: IngestionStatus) {
  switch (status) {
    case "pending":
      return "Pending";

    case "running":
      return "Indexing";

    case "completed":
      return "Completed";

    case "failed":
      return "Failed";

    default:
      return status;
  }
}

export function RepositoryIngestion({
  repositoryId,
  repositoryStatus,
  onCompleted,
}: RepositoryIngestionProps) {
  const [job, setJob] =
    useState<IngestionJob | null>(null);

  const [starting, setStarting] = useState(false);

  const [error, setError] =
    useState<string | null>(null);

  /*
   * If repository was already indexed before
   * opening this page, show it as completed.
   */
  const alreadyIndexed =
    repositoryStatus === "completed";

  async function handleStart() {
    setStarting(true);
    setError(null);

    try {
      const createdJob =
        await startIngestion(repositoryId);

      setJob(createdJob);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to start ingestion",
      );
    } finally {
      setStarting(false);
    }
  }

  /*
   * Poll ingestion job while it is pending/running.
   */
  useEffect(() => {
    if (!job) {
      return;
    }

    if (
      job.status === "completed" ||
      job.status === "failed"
    ) {
      return;
    }

    const intervalId = window.setInterval(
      async () => {
        try {
          const updatedJob =
            await getIngestionJob(job.id);

          setJob(updatedJob);

          if (
            updatedJob.status === "completed"
          ) {
            onCompleted?.();
          }
        } catch (error) {
          setError(
            error instanceof Error
              ? error.message
              : "Failed to check ingestion status",
          );
        }
      },
      2000,
    );

    return () => {
      window.clearInterval(intervalId);
    };
  }, [job, onCompleted]);

  const isRunning =
    job?.status === "pending" ||
    job?.status === "running";

  const isCompleted =
    job?.status === "completed" ||
    alreadyIndexed;

  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6">
      <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold">
            Repository indexing
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Index the repository so the AI can
            understand and search its code.
          </p>
        </div>

        <button
          type="button"
          onClick={handleStart}
          disabled={
            starting ||
            isRunning
          }
          className="shrink-0 rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {starting
            ? "Starting..."
            : isRunning
              ? "Indexing..."
              : isCompleted
                ? "Re-index repository"
                : "Index repository"}
        </button>
      </div>

      {job && (
        <div className="mt-6 rounded-lg border border-gray-200 bg-gray-50 p-4">
          <div className="flex items-center justify-between gap-4">
            <span className="text-sm font-medium">
              Ingestion status
            </span>

            <span
              className={`text-sm font-medium ${
                job.status === "completed"
                  ? "text-green-600"
                  : job.status === "failed"
                    ? "text-red-600"
                    : "text-gray-700"
              }`}
            >
              {statusLabel(job.status)}
            </span>
          </div>

          {job.status === "pending" && (
            <p className="mt-2 text-sm text-gray-500">
              Your ingestion job has been created
              and is waiting to start.
            </p>
          )}

          {job.status === "running" && (
            <div className="mt-3">
              <p className="text-sm text-gray-500">
                Cloning, analyzing, chunking and
                embedding repository files...
              </p>

              <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-gray-200">
                <div className="h-full w-1/2 animate-pulse rounded-full bg-black" />
              </div>
            </div>
          )}

          {job.status === "completed" && (
            <p className="mt-2 text-sm text-green-600">
              Repository indexed successfully.
              You can now ask questions about the
              codebase.
            </p>
          )}

          {job.status === "failed" && (
            <div className="mt-2">
              <p className="text-sm text-red-600">
                Repository ingestion failed.
              </p>

              {job.error_message && (
                <pre className="mt-2 max-h-40 overflow-auto whitespace-pre-wrap rounded bg-red-50 p-3 text-xs text-red-700">
                  {job.error_message}
                </pre>
              )}
            </div>
          )}
        </div>
      )}

      {!job && alreadyIndexed && (
        <div className="mt-6 rounded-lg border border-green-200 bg-green-50 p-4">
          <p className="text-sm text-green-700">
            This repository has already been
            indexed.
          </p>
        </div>
      )}

      {error && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700"
        >
          {error}
        </div>
      )}
    </section>
  );
}
