using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Extensions;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Route("api/open/{companyId:int}/general")]
    [ApiController]
    public class OpenGeneralController : BaseController
    {
        public OpenGeneralController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/open/{companyId}/general/get-info
        /// </summary>
        [HttpGet("get-info")]
        public async Task<ActionResult> Info([FromRoute] int companyId)
        {
            // Retrieve relevant company
            var company = await DbContext.Companies
                .Include(company => company.Pages)
                .AsSplitQuery()
                .AsNoTracking()
                .FirstOrDefaultAsync(company => company.Id == companyId);

            var pages = company.Pages
                .OrderBy(page => page.Order);
            
            // Return view model of general info
            return Ok(new
            {
                CompanyName = company.Name,
                CompanyColor = company.Color,
                CompanyLogo = company.Logo.IsNullOrEmpty() ? "" : await _imageService.DownloadImageURL(company.Logo),
                pages = pages.Select(page => new
                {
                    page.Id,
                    page.Name,
                    page.URLName
                })
            });
        }
    }
}