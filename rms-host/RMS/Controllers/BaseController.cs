using System;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Models;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    public class BaseController : Controller
    {
        protected readonly DbContext DbContext;

        protected readonly IImageService _imageService;
        
        public BaseController(DbContext databaseContext, IImageService imageService)
        {
            DbContext = databaseContext;
            _imageService = imageService;
        }
        
        protected async Task<User> getCurrentUser()
        {
            var userIdClaim = HttpContext.User.Claims.FirstOrDefault(claim => claim.Type == ClaimTypes.PrimarySid);

            if (userIdClaim == null)
            {
                throw new Exception("Tried getting unauthenticated user");
            }
            
            var userId = int.Parse(userIdClaim.Value);

            return await DbContext.Users
                .Include(user => user.Company)
                .ThenInclude(company => company.CompanyModules)
                .FirstOrDefaultAsync(user => user.Id == userId);
        }

        protected async Task<Company> getCurrentUserCompany()
        {
            var userIdClaim = HttpContext.User.Claims
                .FirstOrDefault(claim => claim.Type == ClaimTypes.PrimarySid);
            
            if (userIdClaim == null)
                throw new Exception("Tried getting unauthenticated user");
            
            var userId = int.Parse(userIdClaim.Value);

            return await DbContext.Companies
                .Include(company => company.Pages)
                .Include(company => company.Products)
                .Include(company => company.Users)
                .AsNoTracking()
                .AsSplitQuery()
                .FirstOrDefaultAsync(company => company.Users.Any(user => user.Id == userId));
        }
    }
}