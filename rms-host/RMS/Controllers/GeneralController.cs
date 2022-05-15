using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMS.Enums;
using RMS.Extensions;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class GeneralController : BaseController
    {
        public GeneralController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/general/get-info
        /// </summary>
        [HttpGet("get-info")]
        public async Task<ViewModels.General.Get.ResponseViewModel> GetInfo()
        {
            var user = await getCurrentUser();

            Dictionary<Role, string> RoleMap = new Dictionary<Role, string>
            {
                { Role.SuperAdmin, "Super admin" },
                { Role.Owner, "Owner" },
                { Role.Employee, "Employee" }
            };
            
            return new ViewModels.General.Get.ResponseViewModel
            {
                FirstName = user.FirstName,
                LastName = user.LastName,
                EmailAddress = user.Email,
                Address = user.Address,
                ProfilePicture = user.ProfilePicture.IsNullOrEmpty() ? "" : await  _imageService.DownloadImageURL(user.ProfilePicture),
                Role = RoleMap[user.Role],
                
                CompanyLogo = user.Company.Logo,
                CompanyColor = user.Company.Color,
                CompanyName = user.Company.Name,
                Modules = user.Company.CompanyModules.Select(companyModule => companyModule.Module).ToList()
            };
        }
    }
}