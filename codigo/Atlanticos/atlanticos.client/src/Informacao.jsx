import React, { useEffect, useState } from 'react'; // Importa o React, useEffect e useState do pacote 'react'
import axios from 'axios'; // Importa o Axios para fazer requisições HTTP

// Componente funcional Informacao que recebe as props 'apiUrl' e 'algorithmName'
const Informacao = ({ algorithmName, distance, timeTaken }) => {
  // Define o estado inicial dos dados com mensagens de carregamento
  const [dados, setDados] = useState({
    algoritmo: '',
    distancia: '',
    tempo: '',
  });

  useEffect(() => {
    setDados({ 
      algoritmo: algorithmName,
      distancia: distance,
      tempo: timeTaken,
    });
  }, [algorithmName, distance, timeTaken]);

  // Retorna a seção de informações com os dados atualizados
  return (
    <section className="informacao">
      <div className="algoritmo">
        <h3>Algoritmo</h3>
        <h2>{algorithmName}</h2> {/* Exibe o nome do algoritmo */}
      </div>
      <div className="distancia">
        <h3>Distância</h3>
        <h2>{distance}</h2> {/* Exibe a distância */}
      </div>
      <div className="tempo">
        <h3>Tempo</h3>
        <h2>{timeTaken}</h2> {/* Exibe o tempo */}
      </div>
    </section>
  );
};

export default Informacao; // Exporta o componente Informacao como padrão
