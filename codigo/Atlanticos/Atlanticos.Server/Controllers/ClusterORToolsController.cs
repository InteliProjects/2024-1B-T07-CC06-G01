﻿using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.IO;

namespace Atlanticos.Server.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ClusterORToolsController : ControllerBase
    {
        [HttpGet("api/orTools")]
        public IActionResult RunPythonScript([FromQuery] int? n_clusters)
        {
            // Caminho do diretório base do projeto
            var baseDirectory = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.FullName;

            // Caminho absoluto do script Python
            var pythonFilePath = Path.Combine(baseDirectory, "codigo", "algoritmos", "ORtools.py");

            // Caminho do diretório onde o script Python está localizado
            var scriptDirectory = Path.GetDirectoryName(pythonFilePath);

            // Caminho do arquivo JSON de resultado
            var resultJsonPath = Path.Combine(baseDirectory, "codigo", "algoritmos", "outputs", "JSON", "ORtools_output.json");

            // Verificar se o script Python existe
            if (!System.IO.File.Exists(pythonFilePath))
            {
                return NotFound($"Script Python não encontrado no caminho: {pythonFilePath}");
            }

            try
            {
                // Configura o processo para executar o Python
                var processStartInfo = new ProcessStartInfo
                {
                    FileName = "python",  // Certifique-se de que o Python esteja no PATH
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    WorkingDirectory = scriptDirectory  // Define o diretório de trabalho
                };

                // Adicione argumentos se n_clusters for fornecido
                if (n_clusters.HasValue)
                {
                    processStartInfo.Arguments = $"\"{pythonFilePath}\" --n_clusters {n_clusters.Value}";
                }
                else
                {
                    processStartInfo.Arguments = $"\"{pythonFilePath}\"";
                }

                // Inicia o processo
                var process = new Process
                {
                    StartInfo = processStartInfo
                };
                process.Start();

                // Lê a saída do processo
                var output = process.StandardOutput.ReadToEnd();
                var error = process.StandardError.ReadToEnd();

                process.WaitForExit();

                if (process.ExitCode != 0)
                {
                    return StatusCode(500, $"Erro ao executar o script Python: {error}");
                }

                // Ler o arquivo JSON de resultado
                if (!System.IO.File.Exists(resultJsonPath))
                {
                    return NotFound($"Arquivo de resultado JSON não encontrado no caminho: {resultJsonPath}");
                }

                var resultJson = System.IO.File.ReadAllText(resultJsonPath);

                //var jsonRespose = Newtonsoft.Json.JsonConvert.DeserializeObject(resultJson);

                // Retornar o conteúdo do arquivo JSON
                return Ok(resultJson);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Erro ao executar o script Python: {ex.Message}");
            }
        }
    }
}
