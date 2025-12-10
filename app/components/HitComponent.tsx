"use client";

import { BaseHit } from "instantsearch.js";
import React from "react";
import { Highlight } from "react-instantsearch";

export const HitComponent: React.FC<BaseHit> = ({ hit }) => {
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