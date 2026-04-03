"use client";

import React from "react";
import { useInstantSearch } from "react-instantsearch";

export const EmptyQueryBoundary: React.FC<{
  children: React.ReactNode;
  fallback: React.ReactNode;
}> = ({ children, fallback }) => {
  const { indexUiState } = useInstantSearch();

  if (!indexUiState.query) {
    return (
      <>
        {fallback}
        <div className="text-center py-12">
          <p className="text-slate-500 dark:text-slate-400">
            Start typing to search the dictionary
          </p>
        </div>
        <div hidden>{children}</div>
      </>
    );
  }

  return children;
};
