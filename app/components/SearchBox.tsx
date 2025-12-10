"use client";

import { useSearchBox } from "react-instantsearch";
import React from "react";

export const SearchBox: React.FC = () => {
  const { query, refine } = useSearchBox();

  return (
    <div>
      <input
        type="text"
        name="search-word"
        value={query}
        onChange={(e) => refine(e.target.value)}
        placeholder="Search in English or ܣܘܪܝܬ"
        className="w-full p-2 border border-gray-300 rounded text-black"
      />
    </div>
  );
};
