import React, { useEffect, useState } from "react";

function App() {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/listings/cheapest")
      .then((res) => res.json())
      .then((data) => setListings(data.results))
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🛍️ Cheapest Listings</h1>
      <table border="1" cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>Title</th>
            <th>Price ($)</th>
            <th>Location</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {listings.map((item, index) => (
            <tr key={index}>
              <td>{item.title}</td>
              <td>{item.price_num}</td>
              <td>{item.location}</td>
              <td>
                <a href={item.url} target="_blank" rel="noreferrer">
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

export default App;
