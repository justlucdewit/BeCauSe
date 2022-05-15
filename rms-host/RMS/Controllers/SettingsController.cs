using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Enums;
using RMS.Extensions;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class SettingsController : BaseController
    {
        public SettingsController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// POST: api/settings
        /// </summary>
        [HttpPost]
        public async Task<ActionResult> SaveSettings([FromBody] ViewModels.Settings.SaveSettings.RequestViewModel request)
        {
            // Get current user
            var currentUser = await getCurrentUser();
            
            // Get the user company from the database
            var dbCompany = await DbContext.Companies
                .FirstOrDefaultAsync(company => company.Id == currentUser.CompanyId);
            
            // Map all of the settings to the props on the company
            dbCompany.Color = request.CompanyColor;
            dbCompany.Name = request.CompanyName;
            
            // Save changes to database
            await DbContext.SaveChangesAsync();
            
            // Return http 200
            return Ok();
        }
        
        /// <summary>
        /// GET: api/settings
        /// </summary>
        [HttpGet]
        public async Task<ActionResult> GetSettings()
        {
            // Get current user
            var currentUser = await getCurrentUser();

            // Return ok result with view model containing
            // all the settings
            return Ok(new
            {
                CompanyName = currentUser.Company.Name,
                CompanyColor = currentUser.Company.Color
            });
        }
    }
}