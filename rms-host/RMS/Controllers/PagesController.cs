using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Enums;
using RMS.Extensions;
using RMS.Models;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class PagesController : BaseController
    {
        public PagesController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/pages/all
        /// </summary>
        [HttpGet("all")]
        public async Task<ActionResult> GetAllPages()
        {
            // Get the current user company
            var currentUserCompany = await getCurrentUserCompany();
            
            // Get the page
            var pages = currentUserCompany.Pages;
            
            // Return the pages
            return Ok(pages.Select(page => new
            {
                page.Id,
                page.Order,
                page.Name,
                page.UserMade,
                page.MarkdownContent,
                page.URLName,
                page.SpecialPageId
            }));
        }
        
        /// <summary>
        /// POST: api/pages/save
        /// </summary>
        [HttpPost("save")]
        public async Task SavePages(List<ViewModels.Pages.Save.RequestViewModel> request)
        {
            // Get the current user
            var currentUser = await getCurrentUser();
            
            // Retrieve all current pages from the database
            var pages = await DbContext.Pages.Where(page => page.CompanyId == currentUser.CompanyId).ToListAsync();
                
            // Delete the current pages from the database
            DbContext.Pages.RemoveRange(pages);
            
            // Incrementation variable
            var i = 0;

            foreach (var page in request)
            {
                // Set the ID if its missing
                if (page.Id == null)
                    page.Id = DbContext.Pages.Max(p => p.Id) + 1;
                
                // Add the page to the db
                await DbContext.Pages.AddAsync(new Page
                {
                    Id = (int) page.Id,
                    Name = page.Name,
                    MarkdownContent = page.MarkdownContent,
                    URLName = page.UrlName,
                    Order = i++,
                    CompanyId = currentUser.CompanyId,
                    UserMade = page.UserMade,
                    SpecialPageId = page.SpecialPageId
                });
            }
            
            // Save the changes to the database
            await DbContext.SaveChangesAsync();
        }
    }
}