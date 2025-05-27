// src/App.js
import React, { useEffect, useState } from "react";

export default function App() {
  const [listings, setListings] = useState([]);
  const [locationFilter, setLocationFilter] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/listings/cheapest")
      .then((res) => res.json())
      .then((data) => {
        setListings(data.results);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  const filteredListings = listings.filter((item) => {
    const price = item.price_num;
    const matchesLocation = locationFilter === "" || item.location === locationFilter;
    const matchesMin = minPrice === "" || price >= parseFloat(minPrice);
    const matchesMax = maxPrice === "" || price <= parseFloat(maxPrice);
    return matchesLocation && matchesMin && matchesMax;
  });

  const uniqueLocations = [...new Set(listings.map((item) => item.location))];

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🛒 Cheapest Listings</h1>

      <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <select
          className="border rounded px-3 py-2"
          value={locationFilter}
          onChange={(e) => setLocationFilter(e.target.value)}
        >
          <option value="">All Locations</option>
          {uniqueLocations.map((loc) => (
            <option key={loc} value={loc}>
              {loc}
            </option>
          ))}
        </select>

        <input
          type="number"
          placeholder="Min Price"
          className="border rounded px-3 py-2"
          value={minPrice}
          onChange={(e) => setMinPrice(e.target.value)}
        />
        <input
          type="number"
          placeholder="Max Price"
          className="border rounded px-3 py-2"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
        />
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">Error: {error.message}</p>}
      {!loading && filteredListings.length === 0 && <p>No listings found.</p>}

      <table className="w-full border">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-3 py-2">Title</th>
            <th className="border px-3 py-2">Price</th>
            <th className="border px-3 py-2">Location</th>
            <th className="border px-3 py-2">Link</th>
          </tr>
        </thead>
        <tbody>
          {filteredListings.map((item, idx) => (
            <tr key={idx} className="hover:bg-gray-50">
              <td className="border px-3 py-2">{item.title}</td>
              <td className="border px-3 py-2">${item.price_num}</td>
              <td className="border px-3 py-2">{item.location}</td>
              <td className="border px-3 py-2">
                <a href={item.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                  View
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
