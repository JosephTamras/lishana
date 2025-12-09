"use client";
import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
import { singleIndex } from "instantsearch.js/es/lib/stateMappings";
import {
  InstantSearch,
  InfiniteHits,
  Configure,
  useSearchBox,
  useInstantSearch,
  Highlight
} from "react-instantsearch";
import React from "react";
import { BaseHit } from "instantsearch.js";

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: process.env.NEXT_PUBLIC_TYPESENSE_API_KEY || "", // Be sure to use the search-only-api-key
    nodes: [
      {
        host: "localhost",
        port: 8108,
        protocol: "http",
      },
    ],
  },
  additionalSearchParameters: {
    query_by: "senses.glosses, canonical_phonetic, forms.phonetic, glosses_embedding, canonical_form, forms.form",
  },
});

const HitComponent: React.FC<BaseHit> = ({ hit }) => {
  console.log(hit);
  return (<div className="p-4 border-b">
    {/* fallback to lemma if no canonical */}
    <h2 className="text-xl font-bold text-black font-syriac">
      <Highlight hit={hit} attribute="canonical_form" />
    </h2>
    <h3 className="text-md font-semibold text-gray-600 font-syriac">
      <Highlight hit={hit} attribute="canonical_phonetic" highlightedTagName="mark" />
    </h3>
    {/* map through senses and have a bullet for each gloss in senses.glosses */}
    <ul className="list-disc list-inside mt-2 font-syriac">
      {hit.senses.map((_sense: any, index: React.Key | null | undefined) => (
        <li key={index} className="text-gray-700">
          <Highlight hit={hit} attribute={`senses.${index}.glosses`} highlightedTagName="mark" />
        </li>
      ))}
    </ul>
  </div>)
};

const SearchBoxComponent: React.FC = () => {
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

const EmptyQueryBoundary: React.FC<{ children: React.ReactNode; fallback: React.ReactNode }> = ({ children, fallback }) => {
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
}

export default function Home() {
  // const searchParams = useSearchParams();
  const indexName = "assyrian_dictionary";

  return (
    <div className="flex justify-center items-center flex-col min-h-screen py-2 bg-white">
      <h1 className="text-3xl font-semibold mb-8 text-black">
        Assyrian-English Dictionary
      </h1>
      <InstantSearch
        indexName={indexName}
        searchClient={typesenseInstantsearchAdapter.searchClient}
        routing={{ stateMapping: singleIndex(indexName) }}
        // key={(searchParams.get("query") as string) || ""}
      >
        <Configure hitsPerPage={10} />
        <div className="flex flex-col w-full max-w-xl px-4">
          <SearchBoxComponent />
          <EmptyQueryBoundary fallback={null}>
            <InfiniteHits hitComponent={HitComponent} showPrevious={false} classNames={{
              loadMore: "text-black"
            }} />
          </EmptyQueryBoundary>
        </div>
      </InstantSearch>
    </div>
  );
}