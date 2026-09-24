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

    setLoading(true);
    setError(null);

    try {
      await createRepository(githubUrl);

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
    <form onSubmit={handleSubmit} className="space-y-4">
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
          className="w-full rounded-md border px-3 py-2"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="rounded-md border px-4 py-2 disabled:opacity-50"
      >
        {loading ? "Adding..." : "Add repository"}
      </button>

      {error && (
        <p
          role="alert"
          className="text-sm"
        >
          {error}
        </p>
      )}
    </form>
  );
}