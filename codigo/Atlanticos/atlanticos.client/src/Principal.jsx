import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import './Principal.css';
import MapComponent from './MapComponent';
import Informacao from './Informacao';
import Historico from './Historico';
import Dropdown from './Dropdown';

const Principal = () => {
  const location = useLocation();
  const markers = location.state?.markers || [];

  const [algorithmName, setAlgorithmName] = useState('');
  const [algorithmResult, setAlgorithmResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [distance, setDistance] = useState(0);
  const [csvPath, setCsvPath] = useState('');

  const options = [
    { label: 'Selecione um Algoritmo', value: { url: '', name: '', output: '' } },
    { label: 'ORTools', value: { url: '/ClusterORTools/api/orTools', name: 'ORTools', output: 'algoritmos/outputs/CSV/ORtools_output.csv' } },
    { label: 'K-Means', value: { url: '/KMeansAlgorithm/api/kMeans', name: 'K-Means', output: 'algoritmos/outputs/CSV/NN_output.csv' } },
  ];

  const downloadCSV = (filename) => {
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', filename);
    a.setAttribute('download', 'rota.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleAlgorithmSelect = (selectedValue) => {
    if (!selectedValue) return;

    setLoading(true);
    setError(null);

    fetch(`https://localhost:7186${selectedValue.url}`)
      .then((response) => {
        if (!response.ok) {
          return response.text().then(text => {
            throw new Error(text || 'Erro ao executar o algoritmo');
          });
        }
        return response.json();
      })
      .then((data) => {
        if (data && Array.isArray(data.response)) {
          setAlgorithmResult(data);
          setResponseData(data.response);

          let totalDistance = 0;
          data.response.forEach((item) => {
            totalDistance += item.objective_value;
          });
          setDistance(totalDistance);

          let totalTime = 0;
          data.response.forEach((item) => {
            totalTime += item.time_taken;
          });
          totalTime = (totalTime / 60) / 24;
          totalTime = totalTime.toFixed(2);
          setTimeTaken(totalTime);

          setCsvPath(selectedValue.output);
        } else {
          throw new Error('Dados da API estão malformados');
        }
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message || 'Erro ao executar o algoritmo');
        setLoading(false);
      });
  };

  useEffect(() => {
    console.log('Response Data:', responseData);
  }, [responseData]);

  useEffect(() => {
    console.log('TimeTaken:', timeTaken);
  }, [timeTaken]);

  useEffect(() => {
    console.log('Distance:', distance);
  }, [distance]);

  useEffect(() => {
    console.log('algorithmName:', algorithmName);
  }, [algorithmName]);

  useEffect(() => {
    console.log('CSV Path:', csvPath);
  }, [csvPath]);

  return (
    <div className="container">
      <header>
        <div className="logo">
          <img src="../assets/logo.png" alt="Atlânticos Logo" />
        </div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><a href="#">Sobre</a></li>
            <li><a href="#">Guia de Utilização</a></li>
            <li><a href="#">Nossa Equipe</a></li>
            <li>
              <a
                className="btn"
                onClick={() => downloadCSV(csvPath)}
              >
                Baixe a rota
              </a>
            </li>
          </ul>
        </nav>
      </header>

      <div className="dropdown-container">
        <Dropdown options={options} onSelect={(value) => {
          setAlgorithmName(value.name);
          handleAlgorithmSelect(value);
        }} />
      </div>

      {loading && <p className="status-message">Executando o algoritmo...</p>}
      {error && <p className="status-message-error">{error}</p>}

      <main>
        <section>
          <Informacao
            algorithmName={algorithmName}
            distance={distance}
            timeTaken={timeTaken}
          />
        </section>

        {algorithmResult && responseData && responseData.length > 0 && (
          <div className="algorithm-result">
            <section className="mapa">
              <MapComponent responseData={responseData} />
            </section>
          </div>
        )}

      </main>
    </div>
  );
};

export default Principal;
