const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export interface Repository {
  id: string;
  github_url: string;
  owner: string;
  name: string;
  default_branch: string | null;
  commit_sha: string | null;
  status: string;
}

export async function createRepository(
  github_url: string,
): Promise<Repository> {
  const response = await fetch(
    `${API_BASE_URL}/api/repositories`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ github_url }),
    },
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(
      data?.detail ?? "Failed to create repository",
      response.status,
    );
  }

  return data;
}

export async function listRepositories(): Promise<Repository[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/repositories`,
    {
      cache: "no-store",
    },
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(
      data?.detail ?? "Failed to load repositories",
      response.status,
    );
  }

  return data;
}