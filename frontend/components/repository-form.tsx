"use client";

import { FormEvent, useState } from "react";

import { createRepository } from "@/lib/api";

interface RepositoryFormProps {
  onCreated: () => void;
}

export function RepositoryForm({
  onCreated,
}: RepositoryFormProps) {
  const [githubUrl, setGithubUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedUrl = githubUrl.trim();

    if (!trimmedUrl) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await createRepository(trimmedUrl);

      setGithubUrl("");
      onCreated();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to add repository",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4"
    >
      <div>
        <label
          htmlFor="github-url"
          className="mb-2 block text-sm font-medium"
        >
          GitHub repository URL
        </label>

        <input
          id="github-url"
          type="url"
          value={githubUrl}
          onChange={(event) =>
            setGithubUrl(event.target.value)
          }
          placeholder="https://github.com/owner/repository"
          required
          disabled={loading}
          className="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:bg-gray-100"
        />
      </div>

      <button
        type="submit"
        disabled={loading || !githubUrl.trim()}
        className="rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Adding..." : "Add repository"}
      </button>

      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700"
        >
          {error}
        </div>
      )}
    </form>
  );
}
