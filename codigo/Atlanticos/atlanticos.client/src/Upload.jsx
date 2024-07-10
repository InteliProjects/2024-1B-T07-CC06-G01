import React from 'react';
import './Upload.css';
import { useNavigate, useLocation } from 'react-router-dom';

function Upload() {
  const navigate = useNavigate();
  const location = useLocation();
  const markers = location.state?.markers || [];

  // Função para lidar com o clique no botão de upload
  const handleUploadClick = () => {
    document.getElementById('upload-csv').click();
  };

  // Função para lidar com a mudança de arquivo no input de upload
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      try {
        const formData = new FormData();
        formData.append('file', file);

        console.log('Uploading file...');

        const response = await fetch('https://localhost:7186/api/Csv/upload', {
          method: 'POST',
          body: formData,
        });

        const responseData = await response.json();
        console.log('Response data:', responseData);

        if (response.ok) {
          console.log('File uploaded successfully, response data:', responseData);
          navigate('/principal', { state: { markers: responseData.markers } });
        } else {
          console.error('Error uploading file, response status:', response.status);
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <div>
      <header>
        <div className="logo">
          <img src="logo.png" alt="Atlânticos Logo" />
        </div>
        <nav>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Sobre</a></li>
            <li><a href="#">Guia de Utilização</a></li>
            <li><a href="#">Nossa Equipe</a></li>
            <li><a href="#" className="btn">Baixe a rota</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <section className="guia">
          <h2>Para utilizar o modelo e realizar a análise das rotas, é preciso fazer o upload de um arquivo .csv contendo os dados dos pontos em que os leituristas passam.</h2>
          <h2> São dois passos simples:</h2>
          <div className="passos">
            <div className="passo">
              <div className="numero">1</div>
              <div className="texto">
                <h3>Upload</h3>
                <p>Efetuar o upload do arquivo .csv e aguardar a análise do algoritmo.</p>
              </div>
            </div>
            <div className="passo">
              <div className="numero">2</div>
              <div className="texto">
                <h3>Visualização</h3>
                <p>Com a finalização dos processos, são dispostos rotas e a comparação referente a diferentes algoritmos.</p>
              </div>
            </div>
          </div>
        </section>
        <section className="upload">
          <button className="upload-btn" id="btn-upload" onClick={handleUploadClick}>Faça Upload</button>
          <p>Ou arraste o arquivo</p>
          <input type="file" id="upload-csv" accept=".csv" style={{ display: 'none' }} onChange={handleFileChange} />
        </section>
      </main>
    </div>
  );
}

export default Upload;
