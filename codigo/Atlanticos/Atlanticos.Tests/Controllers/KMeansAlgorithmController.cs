using Atlanticos.Server.Controllers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.VisualStudio.TestPlatform.TestHost;
using Moq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Xunit;

namespace Atlanticos.Tests.Controllers
{
    public class KMeansAlgorithmController : IClassFixture<CustomWebApplicationFactory<Startup>>
    {
        private readonly HttpClient _client;

        public KMeansAlgorithmController(CustomWebApplicationFactory<Startup> factory)
        {
            // Cria o HttpClient com as opções padrão
            _client = factory.CreateClient();

            // Define o timeout do HttpClient
            _client.Timeout = TimeSpan.FromMinutes(5); // Aumenta o timeout para 5 minutos
            _client.BaseAddress = new Uri("https://localhost:5173");
        }

        [Fact]
        public async Task RunPythonScript_ReturnsOkResult()
        {
            // Act
            var response = await _client.GetAsync("/ClusterORTools/api/orTools");

            Console.WriteLine(response.StatusCode);
            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            var responseString = await response.Content.ReadAsStringAsync();
            Assert.Contains("result", responseString);
        }

        [Fact]
        public async Task RunPythonScript_ReturnsNotFound_WhenScriptNotFound()
        {
            // Act
            var response = await _client.GetAsync("/ClusterORTools/api/orTools");

            // Assert
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }

        // Outros testes podem ser adicionados aqui para diferentes cenários
    }
}
