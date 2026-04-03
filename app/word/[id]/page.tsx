"use client";

import React from "react";
import Link from "next/link";
import { singleIndex } from "instantsearch.js/es/lib/stateMappings";
import { Configure, Index, useHits } from "react-instantsearch";
import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
import { InstantSearch } from "react-instantsearch";

interface Form {
  form: string;
  phonetic: string;
}

interface Sense {
  glosses: string;
}

interface Word {
  id: string;
  canonical_form: string;
  canonical_phonetic: string;
  senses: Sense[];
  forms?: Form[];
}

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: process.env.NEXT_PUBLIC_TYPESENSE_API_KEY || "",
    nodes: [
      {
        url: process.env.NEXT_PUBLIC_TYPESENSE_URL || "",
      },
    ],
  },
  additionalSearchParameters: {
    query_by:
      "senses.glosses, canonical_phonetic, forms.phonetic, glosses_embedding, canonical_form, forms.form",
  },
});

const WordDetail: React.FC<{ id: string }> = ({ id }) => {
  const { hits } = useHits();

  const word = hits.find((hit) => (hit as unknown as Word).id === id) as Word | undefined;

  if (!word) {
    return (
      <div className="py-12 px-4 text-center">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-50 mb-4">
          Word not found
        </h2>
        <Link
          href="/"
          className="text-blue-600 dark:text-blue-400 hover:underline"
        >
          Back to search
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-3 sm:px-4">
      <div className="mb-4 sm:mb-6">
        <Link
          href="/"
          className="text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-2 text-sm sm:text-base py-2 px-2 -ml-2 active:bg-slate-100 dark:active:bg-slate-800 rounded transition-colors"
        >
          <svg
            className="w-4 h-4 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Back to search
        </Link>
      </div>

      <div className="bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-700 p-4 sm:p-6">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-900 dark:text-slate-50 font-syriac mb-2 break-words">
          {word.canonical_form}
        </h1>
        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 font-syriac mb-6 break-words">
          {word.canonical_phonetic}
        </p>

        {/* Senses and Definitions */}
        <div className="mb-6 sm:mb-8">
          <h2 className="text-lg sm:text-xl font-semibold text-slate-900 dark:text-slate-50 mb-3 sm:mb-4">
            Definitions
          </h2>
          <ul className="space-y-2 text-sm sm:text-base">
            {word.senses?.map((sense: Sense, index: number) => (
              <li
                key={index}
                className="list-disc list-inside text-slate-700 dark:text-slate-300 ml-2 break-words"
              >
                {sense.glosses}
              </li>
            ))}
          </ul>
        </div>

        {/* Related Forms */}
        {word.forms && word.forms.length > 0 && (
          <div className="mb-6 sm:mb-8">
            <h2 className="text-lg sm:text-xl font-semibold text-slate-900 dark:text-slate-50 mb-3 sm:mb-4">
              Related Forms
            </h2>
            <div className="grid grid-cols-1 gap-3 text-sm sm:text-base">
              {word.forms.map((form: Form, index: number) => (
                <div
                  key={index}
                  className="p-3 sm:p-4 bg-white dark:bg-slate-800 rounded border border-slate-200 dark:border-slate-700"
                >
                  <p className="font-semibold text-slate-900 dark:text-slate-50 font-syriac break-words">
                    {form.form}
                  </p>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 break-words">
                    {form.phonetic}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Raw Data */}
        <details className="text-xs sm:text-sm">
          <summary className="cursor-pointer text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 py-2 px-2 -ml-2 active:bg-slate-100 dark:active:bg-slate-800 rounded transition-colors">
            More Information
          </summary>
          <pre className="mt-4 p-3 sm:p-4 bg-white dark:bg-slate-800 rounded border border-slate-200 dark:border-slate-700 overflow-auto text-xs max-w-full">
            {JSON.stringify(word, null, 2)}
          </pre>
        </details>
      </div>
    </div>
  );
};

export default function WordPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = React.use(params);

  return (
    <div className="flex justify-center items-start flex-col min-h-screen py-4 sm:py-8 bg-white dark:bg-slate-950">
      <div className="w-full">
        <InstantSearch
          indexName={"assyrian_dictionary"}
          searchClient={typesenseInstantsearchAdapter.searchClient}
          routing={{ stateMapping: singleIndex("assyrian_dictionary") }}
        >
          <Configure hitsPerPage={1000} />
          <Index indexName="assyrian_dictionary">
            <WordDetail id={resolvedParams.id} />
          </Index>
        </InstantSearch>
      </div>
    </div>
  );
}
