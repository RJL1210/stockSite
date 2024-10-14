import React, { useEffect, useState } from 'react';

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch('/api/stocks/')
      .then(response => response.json())
      .then(data => setStocks(data));
  }, []);

  return (
    <div className="App">
      <h1>Stocks</h1>
      <ul>
        {stocks.map(stock => (
          <li key={stock.id}>{stock.company_name}: ${stock.price}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;