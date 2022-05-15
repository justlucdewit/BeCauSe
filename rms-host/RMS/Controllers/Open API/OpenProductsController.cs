using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Extensions;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Route("api/open/{companyId:int}/products")]
    [ApiController]
    public class OpenProductsController : BaseController
    {
        public OpenProductsController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/open/{companyId}/products/all
        /// </summary>
        [HttpGet("all")]
        public async Task<ActionResult> GetAllProducts([FromRoute] int companyId)
        {
            // Retrieve relevant company
            var products = await DbContext.Products
                .Where(product => product.CompanyId == companyId)
                .Include(product => product.Company)
                .ToListAsync();

            foreach (var product in products)
            {
                if (!product.Image.IsNullOrEmpty())
                    product.Image = await _imageService.DownloadImageURL(product.Image);
            }
            
            // Return view model of general info
            return Ok(products.Select(product => new ViewModels.Open_API.OpenProducts.GetAllProducts.ResponseViewModel
            {
                BasePrice = product.BasePrice,
                CompanyName = product.Company.Name,
                Description = product.Description,
                Id = product.Id,
                Image = product.Image,
                Name = product.Name
            }));
        }
        
        /// <summary>
        /// GET: api/open/{companyId}/products/{productId}
        /// </summary>
        [HttpGet("{productId:int}")]
        public async Task<ActionResult> GetProduct([FromRoute] int companyId, [FromRoute] int productId)
        {
            // Retrieve relevant company
            var product = await DbContext.Products
                .FirstOrDefaultAsync(product => product.Id == productId && product.CompanyId == companyId);

            if (!product.Image.IsNullOrEmpty())
                product.Image = await _imageService.DownloadImageURL(product.Image);

            // Return view model of general info
            return Ok(product);
        }
    }
}