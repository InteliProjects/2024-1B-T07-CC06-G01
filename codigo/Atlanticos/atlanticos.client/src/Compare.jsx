import React from 'react';
import './Compare.css'; // Importa o arquivo CSS para estilização
import MapComponent from './MapComponent'; // Importa o componente de mapa
import { useLocation } from 'react-router-dom'; // Importa o hook useLocation do react-router-dom

const Compare = () => {
  // Utiliza o hook useLocation para obter a localização atual e acessa o estado passado via navegação
  const location = useLocation();
  const markers = location.state?.markers || []; // Obtém os marcadores do estado ou um array vazio se não existirem

  return (
    <div className="container">
      <header>
        <div className="logo">
          <img src="logo.png" alt="Atlânticos Logo" /> {/* Exibe a logo */}
        </div>
        <nav>
          <ul>
            <li><a href="#">Home</a></li> {/* Link para Home */}
            <li><a href="#">Sobre</a></li> {/* Link para Sobre */}
            <li><a href="#">Guia de Utilização</a></li> {/* Link para Guia de Utilização */}
            <li><a href="#">Nossa Equipe</a></li> {/* Link para Nossa Equipe */}
            <li><a href="#" className="btn">Baixe a rota</a></li> {/* Botão para baixar a rota */}
          </ul>
        </nav>
      </header>

      <main>
        {/* Primeira seção de mapa */}
        <section className="mapa" id="mapa1">
          <div className="informacao">
            <div className="algoritmo">
              <h3>Algoritmo</h3>
              <h2>Colônia de Formigas</h2> {/* Nome do algoritmo */}
            </div>
            <div className="distancia">
              <h3>Distância</h3>
              <h2>10003462 km</h2> {/* Distância */}
            </div>
            <div className="tempo">
              <h3>Tempo</h3>
              <h2>22 Dias</h2> {/* Tempo */}
            </div>
            <div className="local">
              <h3>Local</h3>
              <h2>Jardim América</h2> {/* Local */}
            </div>
          </div>
          <MapComponent markers={markers} /> {/* Componente de mapa com marcadores */}
        </section>

        {/* Segunda seção de mapa */}
        <section className="mapa" id="mapa2">
          <div className="informacao">
            <div className="algoritmo">
              <h3>Algoritmo</h3>
              <h2>Colônia de Formigas</h2> {/* Nome do algoritmo */}
            </div>
            <div className="distancia">
              <h3>Distância</h3>
              <h2>10003462 km</h2> {/* Distância */}
            </div>
            <div className="tempo">
              <h3>Tempo</h3>
              <h2>22 Dias</h2> {/* Tempo */}
            </div>
            <div className="local">
              <h3>Local</h3>
              <h2>Jardim América</h2> {/* Local */}
            </div>
          </div>
          <MapComponent markers={markers} /> {/* Componente de mapa com marcadores */}
        </section>

        {/* Seção de histórico */}
        <section className="historico">
          <h3>Históricos</h3>
          <table>
            <thead>
              <tr>
                <th>Algoritmo</th>
                <th>Distância</th>
                <th>Tempo</th>
                <th>Local</th>
              </tr>
            </thead>
            <tbody>
              {/* Linha do histórico */}
              <tr>
                <td>Clarke y Weight</td>
                <td>108374656 km</td>
                <td>21 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>Colônia de Formigas</td>
                <td>108364655 km</td>
                <td>21 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>Simulated Annealing</td>
                <td>128374656 km</td>
                <td>22 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>Algoritmo Genético</td>
                <td>158374656 km</td>
                <td>19 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>PSO</td>
                <td>188374656 km</td>
                <td>21 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>Clarke y Weight</td>
                <td>408374656 km</td>
                <td>21 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>Clarke y Weight</td>
                <td>148374656 km</td>
                <td>21 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
              <tr>
                <td>Clarke y Weight</td>
                <td>258374656 km</td>
                <td>21 dias, 5 horas</td>
                <td>Jardim América</td>
              </tr>
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
};

export default Compare; // Exporta o componente Compare como padrão
