using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Route("api/open/{companyId:int}/pages")]
    [ApiController]
    public class OpenPagesController : BaseController
    {
        public OpenPagesController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/open/{companyId}/pages/{pageId}
        /// </summary>
        [HttpGet("{pageId:int}")]
        public async Task<ActionResult> Info([FromRoute] int pageId)
        {
            var page = await DbContext.Pages
                .FirstOrDefaultAsync(pages => pages.Id == pageId);
            
            // Return view model of page info
            return Ok(new
            {
                page.Name,
                page.Id,
                page.Order,
                page.MarkdownContent,
                page.UserMade,
                page.URLName,
                page.SpecialPageId
            });
        }
    }
}