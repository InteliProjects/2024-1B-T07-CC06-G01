import { useEffect, useState } from 'react';
import './App.css';

// Arquivo principal do front-end
function App() {
    // Declaração de um estado chamado "forecasts" com a função "setForecasts" para atualizá-lo
    const [forecasts, setForecasts] = useState();

    // useEffect para chamar a função "populateWeatherData" quando o componente for montado
    useEffect(() => {
        populateWeatherData();
    }, []);

    // Se "forecasts" for indefinido, exibe uma mensagem de carregando
    // Caso contrário, exibe uma tabela com os dados do tempo
    const contents = forecasts === undefined
        ? <p><em>Loading... Please refresh once the ASP.NET backend has started. See <a href="https://aka.ms/jspsintegrationreact">https://aka.ms/jspsintegrationreact</a> for more details.</em></p>
        : <table className="table table-striped" aria-labelledby="tabelLabel">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Temp. (C)</th>
                    <th>Temp. (F)</th>
                    <th>Summary</th>
                </tr>
            </thead>
            <tbody>
                {/* Mapeia os dados de "forecasts" para criar linhas da tabela */}
                {forecasts.map(forecast =>
                    <tr key={forecast.date}>
                        <td>{forecast.date}</td>
                        <td>{forecast.temperatureC}</td>
                        <td>{forecast.temperatureF}</td>
                        <td>{forecast.summary}</td>
                    </tr>
                )}
            </tbody>
        </table>;

    return (
        <div>
            <h1 id="tabelLabel">Weather forecast</h1>
            <p>This component demonstrates fetching data from the server.</p>
            {contents}
        </div>
    );
    
    // Função assíncrona para buscar dados do tempo do servidor
    async function populateWeatherData() {
        const response = await fetch('weatherforecast'); // Faz uma requisição à URL 'weatherforecast'
        const data = await response.json(); // Converte a resposta em JSON
        setForecasts(data); // Atualiza o estado "forecasts" com os dados recebidos
    }
}

export default App;
