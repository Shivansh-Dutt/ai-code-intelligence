"use client";

import {
  FormEvent,
  useState,
} from "react";

import {
  askRepository,
  ApiError,
  AskResponse,
} from "@/lib/api";

interface RepositoryQAProps {
  repositoryId: string;
}

export function RepositoryQA({
  repositoryId,
}: RepositoryQAProps) {
  const [question, setQuestion] = useState("");

  const [result, setResult] =
    useState<AskResponse | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedQuestion =
      question.trim();

    if (!trimmedQuestion) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response =
        await askRepository(
          repositoryId,
          trimmedQuestion,
        );

      setResult(response);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(
          `${err.message} (${err.status})`,
        );
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      {/* Question */}
      <section className="rounded-xl border border-gray-200 bg-white p-6">
        <div className="mb-5">
          <h2 className="text-lg font-semibold">
            Ask about this repository
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Ask questions about the indexed
            codebase.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-4"
        >
          <textarea
            id="repository-question"
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="Where is authentication handled?"
            rows={5}
            disabled={loading}
            className="w-full resize-y rounded-lg border border-gray-300 bg-white p-4 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:opacity-60"
          />

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={
                loading ||
                !question.trim()
              }
              className="rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Thinking..."
                : "Ask"}
            </button>

            {loading && (
              <span className="text-sm text-gray-500">
                Searching repository...
              </span>
            )}
          </div>
        </form>
      </section>

      {/* Error */}
      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700"
        >
          {error}
        </div>
      )}

      {/* Answer */}
      {result && (
        <section className="space-y-6">
          <div>
            <h2 className="mb-3 text-lg font-semibold">
              Answer
            </h2>

            <div className="rounded-xl border border-gray-200 bg-white p-5">
              <div className="whitespace-pre-wrap text-sm leading-7">
                {result.answer}
              </div>
            </div>
          </div>

          {/* Sources */}
          <div>
            <h2 className="mb-3 text-lg font-semibold">
              Sources
            </h2>

            {result.sources.length === 0 ? (
              <div className="rounded-xl border border-gray-200 p-4 text-sm text-gray-500">
                No source files were returned.
              </div>
            ) : (
              <div className="space-y-3">
                {result.sources.map(
                  (source) => (
                    <div
                      key={source.chunk_id}
                      className="rounded-xl border border-gray-200 bg-white p-4"
                    >
                      <div className="flex items-center justify-between gap-4">
                        <div className="min-w-0">
                          <div className="truncate font-mono text-sm font-medium">
                            {source.path}
                          </div>

                          <div className="mt-1 text-xs text-gray-500">
                            Lines{" "}
                            {source.start_line}–
                            {source.end_line}
                          </div>
                        </div>

                        <div className="shrink-0 text-xs text-gray-400">
                          distance{" "}
                          {source.distance.toFixed(
                            3,
                          )}
                        </div>
                      </div>
                    </div>
                  ),
                )}
              </div>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
