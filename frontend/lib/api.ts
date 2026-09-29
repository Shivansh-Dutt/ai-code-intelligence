const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/* ─────────────────────────────────────
   Repository
───────────────────────────────────── */

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

export async function listRepositories(): Promise<
  Repository[]
> {
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

/* ─────────────────────────────────────
   Ingestion
───────────────────────────────────── */

export type IngestionStatus =
  | "pending"
  | "running"
  | "completed"
  | "failed";

export interface IngestionJob {
  id: string;
  repository_id: string;
  status: IngestionStatus;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export async function startIngestion(
  repositoryId: string,
): Promise<IngestionJob> {
  const response = await fetch(
    `${API_BASE_URL}/api/repositories/${repositoryId}/ingest`,
    {
      method: "POST",
    },
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(
      data?.detail ??
        "Failed to start repository ingestion",
      response.status,
    );
  }

  return data;
}

export async function getIngestionJob(
  jobId: string,
): Promise<IngestionJob> {
  const response = await fetch(
    `${API_BASE_URL}/api/ingestion-jobs/${jobId}`,
    {
      cache: "no-store",
    },
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(
      data?.detail ??
        "Failed to load ingestion status",
      response.status,
    );
  }

  return data;
}

/* ─────────────────────────────────────
   Repository Q&A
───────────────────────────────────── */

export interface Source {
  chunk_id: string;
  file_id: string;
  path: string;
  start_line: number;
  end_line: number;
  distance: number;
}

export interface AskResponse {
  answer: string;
  sources: Source[];
}

export async function askRepository(
  repositoryId: string,
  question: string,
): Promise<AskResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/repositories/${repositoryId}/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    },
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(
      data?.detail ?? "Failed to ask repository",
      response.status,
    );
  }

  return data;
}
