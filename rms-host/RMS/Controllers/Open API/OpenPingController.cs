using Microsoft.AspNetCore.Mvc;

namespace RMS.Controllers
{
    [Route("api/ping")]
    [ApiController]
    public class OpenPingController : Controller
    {
        /// <summary>
        /// GET: api/ping
        /// </summary>
        [HttpGet]
        public ActionResult Ping()
        {
            return Ok("pong");
        }
    }
}