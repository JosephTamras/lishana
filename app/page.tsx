"use client";

import { singleIndex } from "instantsearch.js/es/lib/stateMappings";
import { Configure, InfiniteHits } from "react-instantsearch";
import { EmptyQueryBoundary } from "./components/EmptyQueryBoundary";
import { SearchBox } from "./components/SearchBox";
import { HitComponent } from "./components/HitComponent";
import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
import { InstantSearch } from "react-instantsearch";

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: process.env.NEXT_PUBLIC_TYPESENSE_API_KEY || "", // Be sure to use the search-only-api-key
    nodes: [
      {
        url: process.env.NEXT_PUBLIC_TYPESENSE_URL || ""
      },
    ],
  },
  additionalSearchParameters: {
    query_by:
      "senses.glosses, canonical_phonetic, forms.phonetic, glosses_embedding, canonical_form, forms.form",
  },
});

export default function Home() {
  // const searchParams = useSearchParams();
  return (
    <div className="flex justify-center items-center flex-col min-h-screen py-4 sm:py-2 bg-white dark:bg-slate-950 transition-colors px-4">
      <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-2 text-slate-900 dark:text-slate-50 text-center">
        Assyrian-English Dictionary
      </h1>
      <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mb-6 sm:mb-8 text-center italic">
        Search by sound, meaning, or definition
      </p>
      <InstantSearch
        indexName={"assyrian_dictionary"}
        searchClient={typesenseInstantsearchAdapter.searchClient}
        routing={{ stateMapping: singleIndex("assyrian_dictionary") }}
      >
        <Configure hitsPerPage={10} />
        <div className="flex flex-col w-full max-w-2xl gap-4 sm:gap-6">
          <SearchBox />
          <EmptyQueryBoundary fallback={null}>
            <div className="bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
              <InfiniteHits
                hitComponent={HitComponent}
                showPrevious={false}
                classNames={{
                  loadMore:
                    "text-slate-900 dark:text-slate-50 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 px-4 py-3 rounded transition-colors w-full font-medium text-sm sm:text-base touch-none",
                }}
              />
            </div>
          </EmptyQueryBoundary>
        </div>
      </InstantSearch>
    </div>
  );
}
