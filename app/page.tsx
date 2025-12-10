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
    <div className="flex justify-center items-center flex-col min-h-screen py-2 bg-white">
      <h1 className="text-3xl font-semibold mb-8 text-black">
        Assyrian-English Dictionary
      </h1>
      <InstantSearch
        indexName={"assyrian_dictionary"}
        searchClient={typesenseInstantsearchAdapter.searchClient}
        routing={{ stateMapping: singleIndex("assyrian_dictionary") }}
      >
        <Configure hitsPerPage={10} />
        <div className="flex flex-col w-full max-w-xl px-4">
          <SearchBox />
          <EmptyQueryBoundary fallback={null}>
            <InfiniteHits
              hitComponent={HitComponent}
              showPrevious={false}
              classNames={{
                loadMore: "text-black",
              }}
            />
          </EmptyQueryBoundary>
        </div>
      </InstantSearch>
    </div>
  );
}
