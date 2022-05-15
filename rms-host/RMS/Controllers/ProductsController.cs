using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Extensions;
using RMS.Models;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class ProductsController : BaseController
    {
        public ProductsController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// api/products/update
        /// </summary>
        [HttpPost("update")]
        public async Task<ActionResult> Update([FromBody] ViewModels.Products.Update.RequestViewModel request)
        {
            var currentUser = await getCurrentUser();
            
            // Create new product
            if (request.Id == null)
            {
                // Create the resource for the product image
                string productImageResource = null;
                if (!request.Image.IsNullOrEmpty())
                    productImageResource = await _imageService.UploadDataURI(request.Image, "Product");

                await DbContext.Products.AddAsync(new Product
                {
                    Name = request.Name,
                    Description = request.Description,
                    Image = productImageResource,
                    CompanyId = currentUser.CompanyId,
                    BasePrice = (float) (Math.Round(request.BasePrice * 100f) / 100f)
                });
            }
            
            // Update existing product
            else
            {
                // Retrieve the product from the database
                var dbProduct = await DbContext.Products
                    .FirstOrDefaultAsync(product =>
                        product.CompanyId == currentUser.CompanyId && product.Id == request.Id);
                
                // Check if that product even exists
                if (dbProduct == null)
                    return NotFound("The product was not found");
                
                // Update the simple values
                dbProduct.Name = request.Name;
                dbProduct.Description = request.Description;
                dbProduct.BasePrice = (float) (Math.Round(request.BasePrice * 100f) / 100f);
                
                // Delete product image if exists
                if (!dbProduct.Image.IsNullOrEmpty())
                    await _imageService.DeleteImageURL(dbProduct.Image);
                
                // Set new product image if needed
                if (!request.Image.IsNullOrEmpty())
                {
                    // Upload the image and set the file id
                    var fileId = await _imageService.UploadDataURI(request.Image, "product");
                    dbProduct.Image = fileId;
                }
            }
            
            // Save changes to database
            await DbContext.SaveChangesAsync();
            
            // Return http 200
            return Ok();
        }
        
        /// <summary>
        /// api/product
        /// </summary>
        /// <returns></returns>
        [HttpGet("")]
        public async Task<ActionResult> GetAll()
        {
            // Get the current user
            var currentUser = await getCurrentUser();
            
            // Get all products of the current user company
            var products = DbContext.Products
                .Where(product => product.CompanyId == currentUser.CompanyId)
                .Select(product => new ViewModels.Products.GetAll.ResponseViewModel
                {
                    Id = product.Id,
                    Name = product.Name,
                    Image = product.Image
                })
                .OrderBy(product => product.Name)
                .ToList();
            
            // Loop over all the products to dereference the image
            foreach (var product in products)
                if (!product.Image.IsNullOrEmpty())
                    product.Image = await _imageService.DownloadImageURL(product.Image);
            
            // Return all of the products
            return Ok(products);
        }
        
        /// <summary>
        /// api/products/{productId}
        /// </summary>
        [HttpGet("{productId:int}")]
        public async Task<ActionResult> Get([FromRoute] int productId)
        {
            // Get the current user
            var currentUser = await getCurrentUser();
            
            // Get the product from the database
            // product must be from the currentUser.company
            var dbProduct = await DbContext.Products
                .Where(product => product.CompanyId == currentUser.CompanyId)
                .FirstOrDefaultAsync(product => product.Id == productId);
            
            // Check if the product was found, if not, return not found
            if (dbProduct == null)
                return NotFound("The product was not found");
            
            // Create the response view model, and dereference the product image
            var response = new ViewModels.Products.Get.ResponseViewModel
            {
                Id = dbProduct.Id,
                Name = dbProduct.Name,
                Description = dbProduct.Description,
                Image = dbProduct.Image.IsNullOrEmpty() ? "" : await _imageService.DownloadImageURL(dbProduct.Image),
                BasePrice = dbProduct.BasePrice
            };
            
            // Return the response viewmodel
            return Ok(response);
        }

        [HttpDelete("{productId:int}")]
        public async Task<ActionResult> Delete([FromRoute] int productId)
        {
            // Get the current user
            var currentUser = await getCurrentUser();
            
            // get the relevant product out of the database
            // it must have the same company as current user
            var dbProduct = await DbContext.Products
                .FirstOrDefaultAsync(product => product.CompanyId == currentUser.CompanyId && product.Id == productId);

            if (dbProduct == null)
                return NotFound("The product was not found");
            
            // Delete the product image if it exists
            if (!dbProduct.Image.IsNullOrEmpty())
                await _imageService.DeleteImageURL(dbProduct.Image);
            
            // Delete the product from the database
            DbContext.Products.Remove(dbProduct);
            
            // Save the changes to the database
            await DbContext.SaveChangesAsync();
            
            // Return http 200
            return Ok();
        }
    }
}