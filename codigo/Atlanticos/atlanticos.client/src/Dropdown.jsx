import React from 'react'; // Importa o React para usar na criação de componentes
import './Dropdown.css'; // Importa o arquivo de estilos CSS para o componente

// Componente de Dropdown que recebe props "options" e "onSelect"
const Dropdown = ({ options, onSelect }) => {
  // Função para lidar com a seleção de uma opção do dropdown
  const handleSelect = (event) => {
    const selectedIndex = event.target.selectedIndex; // Obtém o índice da opção selecionada
    onSelect(options[selectedIndex].value); // Chama a função onSelect passando o valor selecionado
  };

  return (
    // Retorna um elemento select (dropdown) com a classe "custom-dropdown" e um evento onChange que chama a função handleSelect
    <select className="custom-dropdown" onChange={handleSelect}>
      {/* Mapeia as opções recebidas e cria um elemento option para cada uma */}
      {options.map((option, index) => (
        <option key={index} value={option.value.url}> {/* Define a chave e o valor da opção */}
          {option.label} {/* Exibe o rótulo da opção */}
        </option>
      ))}
    </select>
  );
};

export default Dropdown; // Exporta o componente Dropdown como padrão
