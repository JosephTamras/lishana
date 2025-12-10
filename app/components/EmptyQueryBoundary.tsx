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
        <div hidden>{children}</div>
      </>
    );
  }

  return children;
};
