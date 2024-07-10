using Microsoft.AspNetCore.Mvc;
using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace Atlanticos.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CsvController : ControllerBase
    {
        private readonly string _projectDirectory = Path.Combine(AppContext.BaseDirectory, "CsvFiles"); // Diretório onde os arquivos CSV serão salvos.

        [HttpPost("upload")]
        public async Task<IActionResult> UploadCsv(IFormFile file)
        {
            try
            {
                // Verifica se o diretório existe, caso contrário, cria-o
                if (!Directory.Exists(_projectDirectory))
                {
                    Directory.CreateDirectory(_projectDirectory);
                }

                // Deleta arquivos CSV existentes no diretório
                string[] existingCsvFiles = Directory.GetFiles(_projectDirectory, "*.csv");
                foreach (var csv in existingCsvFiles)
                {
                    System.IO.File.Delete(csv);
                }

                // Salva novos arquivos CSV
                await SaveCsvFile(file, "data.csv");

                // Aqui você pode preparar os dados que deseja enviar de volta como resposta
                var responseData = new
                {
                    message = "CSV files uploaded successfully.",
                    // Adicione outros dados relevantes aqui
                };

                return Ok(responseData); // Retorna sucesso como JSON.
            }
            catch (Exception ex)
            {
                var errorResponse = new
                {
                    message = $"Internal server error: {ex.Message}"
                };
                return StatusCode(500, errorResponse); // Retorna erro interno do servidor como JSON.
            }
        }

        // Método para salvar arquivos CSV no diretório do projeto
        private async Task SaveCsvFile(IFormFile file, string fileName)
        {
            try
            {
                if (file != null && file.Length > 0)
                {
                    // Verifica se o arquivo possui extensão CSV
                    if (Path.GetExtension(file.FileName).ToLower() != ".csv")
                    {
                        throw new Exception("Uploaded file is not a CSV file."); // Lança exceção se não for um arquivo CSV.
                    }

                    string filePath = Path.Combine(_projectDirectory, fileName); // Caminho completo do arquivo.
                    using (var stream = new FileStream(filePath, FileMode.Create))
                    {
                        await file.CopyToAsync(stream); // Copia o conteúdo do arquivo para o stream.
                    }
                }
                else
                {
                    throw new Exception("No file was uploaded or the file is empty.");
                }
            }
            catch (Exception ex)
            {
                throw new Exception($"Error saving CSV file '{fileName}': {ex.Message}"); // Lança exceção em caso de erro ao salvar o arquivo.
            }
        }
    }
}
