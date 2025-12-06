"use client";
import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
import { singleIndex } from "instantsearch.js/es/lib/stateMappings";
import {
  InstantSearch,
  InfiniteHits,
  Configure,
  useSearchBox,
  useInstantSearch
} from "react-instantsearch";
import React from "react";

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
    // query_by: "senses.glosses, forms.phonetic, glosses_embedding, forms.form, word",
    query_by: "glosses_embedding",
  },
});

interface Hit {
  word: string;
  senses: Array<any>;
  canonical: string;
  canonical_phonetic: string;
}


const SimplifiedHit = (hit: any) =>{
  return {
    word: hit.word,
    senses: hit.senses,
    forms: hit.forms,
    // take the form whose tags has "canonical"
    canonical: hit.forms.find((form: any) => form.tags.includes("canonical"))?.form || hit.word,
    canonical_phonetic: hit.forms.find((form: any) => form.tags.includes("canonical"))?.phonetic || "",
  } as Hit;
}

interface HitComponentProps {
  hit: Hit;
}

const HitComponent: React.FC<HitComponentProps> = ({ hit }) => {
  const simplifiedHit = SimplifiedHit(hit);
  return (<div className="p-4 border-b">
    {/* fallback to lemma if no canonical */}
    <h2 className="text-xl font-bold text-black">{simplifiedHit.canonical}</h2>
    <h3 className="text-md font-semibold text-gray-600">{simplifiedHit.canonical_phonetic}</h3>
    {/* map through senses and have a bullet for each gloss in senses.glosses */}
    <ul className="list-disc list-inside mt-2">
      {simplifiedHit.senses.map((sense, index) => (
        <li key={index} className="text-gray-700">
          {sense.glosses.join(", ")}
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
        <Configure hitsPerPage={10}/>
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