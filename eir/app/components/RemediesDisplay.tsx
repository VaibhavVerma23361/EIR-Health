'use client';

import { useState } from 'react';
import { remedies, searchRemedies, Remedy } from '../utils/remedies';

export default function RemediesDisplay() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [expandedRemedy, setExpandedRemedy] = useState<number | null>(null);

  const categories = [
    'all', 'skin', 'hair', 'digestive', 'respiratory', 
    'pain', 'circulation', 'oral', 'general'
  ];

  const filteredRemedies = searchTerm 
    ? searchRemedies(searchTerm)
    : remedies;

  const toggleExpand = (id: number) => {
    setExpandedRemedy(expandedRemedy === id ? null : id);
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          Natural Home Remedies
        </h2>
        <p className="text-gray-600 mb-6">
          Discover traditional remedies for common ailments using natural ingredients
        </p>
        
        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <input
            type="text"
            placeholder="Search remedies..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="text-sm text-gray-600">
          Showing {filteredRemedies.length} of {remedies.length} remedies
        </div>
      </div>

      {/* Remedies Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredRemedies.map((remedy) => (
          <div
            key={remedy.id}
            className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-xl font-semibold text-gray-800">
                  {remedy.ailment}
                </h3>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                  #{remedy.id}
                </span>
              </div>
              
              <h4 className="text-lg font-medium text-green-600 mb-2">
                {remedy.remedy}
              </h4>
              
              <div className="space-y-3 text-sm">
                <div>
                  <span className="font-semibold text-gray-700">Ingredients:</span>
                  <p className="text-gray-600">{remedy.ingredients}</p>
                </div>
                
                {expandedRemedy === remedy.id && (
                  <>
                    <div>
                      <span className="font-semibold text-gray-700">Instructions:</span>
                      <p className="text-gray-600">{remedy.instructions}</p>
                    </div>
                    
                    <div>
                      <span className="font-semibold text-orange-600">⚠️ Caution:</span>
                      <p className="text-orange-600">{remedy.caution}</p>
                    </div>
                    
                    <div>
                      <span className="font-semibold text-blue-600">💡 Note:</span>
                      <p className="text-blue-600">{remedy.note}</p>
                    </div>
                  </>
                )}
              </div>
              
              <button
                onClick={() => toggleExpand(remedy.id)}
                className="mt-4 w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200"
              >
                {expandedRemedy === remedy.id ? 'Show Less' : 'View Details'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredRemedies.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">
            No remedies found for "{searchTerm}"
          </p>
        </div>
      )}
    </div>
  );
}
