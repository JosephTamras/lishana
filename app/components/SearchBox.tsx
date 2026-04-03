"use client";

import { useSearchBox } from "react-instantsearch";
import React from "react";

export const SearchBox: React.FC = () => {
  const { query, refine } = useSearchBox();
  const MAX_SEARCH_LENGTH = 100;

  const handleClear = () => {
    refine("");
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value.length <= MAX_SEARCH_LENGTH) {
      refine(value);
    }
  };

  return (
    <div className="w-full">
      <div className="relative flex items-center">
        <svg
          className="absolute left-3 w-5 h-5 text-slate-400 dark:text-slate-500 pointer-events-none flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          type="text"
          name="search-word"
          value={query}
          onChange={handleChange}
          maxLength={MAX_SEARCH_LENGTH}
          placeholder="Search in English or ܣܘܪܝܬ"
          className="w-full pl-10 pr-12 py-3 sm:py-3 text-base sm:text-base border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-50 placeholder-slate-500 dark:placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        />
        {query && (
          <button
            onClick={handleClear}
            className="absolute right-3 p-2 -m-2 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors active:bg-slate-100 dark:active:bg-slate-700 rounded"
            aria-label="Clear search"
            title="Clear search"
          >
            <svg
              className="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};
