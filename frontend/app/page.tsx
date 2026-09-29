"use client";

import { useState } from "react";

import { RepositoryForm } from "@/components/repository-form";
import { RepositoryList } from "@/components/repository-list";

export default function Home() {
  const [refreshKey, setRefreshKey] =
    useState(0);

  function handleRepositoryCreated() {
    setRefreshKey(
      (value) => value + 1,
    );
  }

  return (
    <main className="mx-auto min-h-screen max-w-4xl px-6 py-12">
      <header>
        <h1 className="text-3xl font-bold">
          AI Code Intelligence
        </h1>

        <p className="mt-2 text-gray-600">
          Add a GitHub repository to begin
          analyzing its codebase.
        </p>
      </header>

      <section className="mt-8 rounded-xl border border-gray-200 bg-white p-6">
        <RepositoryForm
          onCreated={
            handleRepositoryCreated
          }
        />
      </section>

      <RepositoryList
        refreshKey={refreshKey}
      />
    </main>
  );
}
