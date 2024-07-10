// Historico.jsx
import React from 'react'; // Importa a biblioteca React


const Historico = () => {
  return ( // Retorna uma seção com a classe "historico"
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
  );
};

export default Historico; // Exporta o componente Historico como padrão
