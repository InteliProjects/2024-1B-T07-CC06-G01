import React from 'react'; // Importa o React
import ReactDOM from 'react-dom/client'; // Importa o ReactDOM para renderizar o aplicativo
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // Importa BrowserRouter, Routes e Route do react-router-dom
import Upload from './Upload'; // Importa o componente Upload
import Principal from './Principal'; // Importa o componente Principal
import Compare from './Compare'; // Importa o componente Compare

const App = () => {
  return (
    <BrowserRouter> {/* Define o BrowserRouter como o componente raiz para o roteamento */}
      <Routes> {/* Define as rotas */}
        <Route path="/" element={<Upload />} /> {/* Rota para o componente Upload */}
        <Route path="/principal" element={<Principal />} /> {/* Rota para o componente Principal */}
        <Route path="/compare" element={<Compare />} /> {/* Rota para o componente Compare */}
      </Routes>
    </BrowserRouter>
  );
};

// Renderiza o aplicativo usando ReactDOM.createRoot para permitir o uso de recursos avançados do React (como Suspense)
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode> {/* Ativa o modo de estrito para identificar e evitar práticas problemáticas */}
    <App /> {/* Renderiza o componente App */}
  </React.StrictMode>
);
