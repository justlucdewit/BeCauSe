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
    public class OrdersController : BaseController
    {
        public OrdersController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/orders
        /// </summary>
        [HttpGet]
        public async Task<ActionResult> GetAllOrders()
        {
            var currentUserCompany = await getCurrentUserCompany();
            
            var ordersQuery = DbContext.Orders
                .Where(x => x.ForCompanyId == currentUserCompany.Id)
                .OrderBy(x => x.PlacedDate);
            
            return Ok(ordersQuery.Select(x => new
            {
                Id = x.Id,
                Status = x.Status,
                PlacedDate = x.PlacedDate
            }));
        }
        
        /// <summary>
        /// GET: api/orders/{orderId}
        /// </summary>
        [HttpGet("{orderId:int}")]
        public async Task<ActionResult> GetOrder([FromRoute] int orderId)
        {
            var order = DbContext.Orders
                .Include(order => order.CustomerDetails)
                .Include(order => order.Items)
                .ThenInclude(item => item.Product)
                .Include(order => order.Items)
                .ThenInclude(item => item.Settings)
                .FirstOrDefault(x => x.Id == orderId);

            if (order == null)
                return NotFound();
            
            return Ok(new
            {
                Id = order.Id,
                Status = order.Status,
                PlacedDate = order.PlacedDate,
                CustomerDetails = order.CustomerDetails.ToDictionary(details => details.Key, details => details.Value),
                Products = order.Items.Select(item => new
                {
                    ProductId = item.Product.Id,
                    Settings = item.Settings.ToDictionary(setting => setting.Key, setting => setting.Value)
                }).ToList()
            });
        }

        /// <summary>
        /// POST: api/orders
        /// </summary>
        [HttpPost]
        public async Task<ActionResult> CreateNewOrder([FromBody] ViewModels.Orders.CreateNewOrder.RequestViewModel request)
        {
            if (!request.CustomerDetails.ContainsKey("email"))
                return BadRequest("Customer details must contain an email");
            
            var currentUserCompany = await getCurrentUserCompany();

            var orderId = DbContext.Orders.Max(o => o.Id) + 1;
            
            var createdOrder = new Order
            {
                Id = orderId,
                Status = request.Status,
                PlacedDate = DateTime.UtcNow,
                ForCompanyId = currentUserCompany.Id,
                Items = request.OrderItems.Select(x => new OrderItem
                {
                    ProductId = x.ProductId,
                    Settings = x.Settings.Select(keyValuePair => new OrderItemSettings
                    {
                        Key = keyValuePair.Key,
                        Value = keyValuePair.Value
                    }).ToList()
                }).ToList(),
                CustomerDetails = request.CustomerDetails.Select(keyValuePair => new CustomerDetails
                {
                    Key = keyValuePair.Key,
                    Value = keyValuePair.Value
                }).ToList()
            };

            DbContext.Orders.Add(createdOrder);
            DbContext.SaveChanges();
            
            createdOrder = DbContext.Orders
                .Include(order => order.CustomerDetails)
                .Include(order => order.Items)
                .ThenInclude(item => item.Product)
                .Include(order => order.Items)
                .ThenInclude(item => item.Settings)
                .FirstOrDefault(x => x.Id == orderId);
            
            // TODO: Send order confirmation
            await SendOrderConfirmation(createdOrder);
            
            return Ok();
        }
        
        /// <summary>
        /// DELETE: api/orders/{orderId}
        /// </summary>
        [HttpDelete("{orderId:int}")]
        public async Task<ActionResult> DeleteOrder([FromRoute] int orderId)
        {
            // Get the order if exists
            var order = DbContext.Orders
                .FirstOrDefault(x => x.Id == orderId);

            if (order == null)
                return NotFound();
            
            // Get the customer details
            var customerDetails = DbContext.CustomerDetails.Where(x => x.OrderId == orderId);
            
            // Get the order items
            var orderItems = DbContext.OrderItems.Where(x => x.OrderId == orderId);
            
            // Get the order item settings
            var orderItemSettings = DbContext.OrderItems.Where(x => x.OrderId == orderId).SelectMany(x => x.Settings);
            
            // Remove all the data
            DbContext.CustomerDetails.RemoveRange(customerDetails);
            DbContext.OrderItems.RemoveRange(orderItems);
            DbContext.OrderItemSettings.RemoveRange(orderItemSettings);
            DbContext.Orders.Remove(order);
            
            // Save database
            DbContext.SaveChanges();
            
            // Confirm cancelation
            await SendOrderCancelation();
            
            return Ok();
        }
        
        /// <summary>
        /// Send an order confirmation to the customer's
        /// email address
        /// </summary>
        private async Task SendOrderCancelation()
        {
            EmailingService.SendEmail("", "", "");
        }
        
        /// <summary>
        /// Send an order confirmation to the customer's
        /// email address
        /// </summary>
        private async Task SendOrderConfirmation(Order order)
        {
            var orderIdString = order.Id.ToString();
            var orderCompany = DbContext.Companies.FirstOrDefault(x => x.Id == order.ForCompanyId);

            var orderListHTML = "";
            
            order.Items.ForEach(item =>
            {
                var productSettings = "";
                
                item.Settings.ForEach(setting =>
                {
                    productSettings += EmailingService.EvaluateTemplate("OrderItemProperty.html", new Dictionary<string, string>
                    {
                        { setting.Key, setting.Value }
                    });
                });
                
                orderListHTML += EmailingService.EvaluateTemplate("OrderItem.html", new Dictionary<string, string>
                {
                    { "background", "red" },
                    { "productName", item.Product.Name },
                    { "productProperties", productSettings }
                });
            });
            
            EmailingService.SendTemplate("OrderConfirmation.html", new Dictionary<string, string>
            {
                { "email", order.CustomerDetails.FirstOrDefault(x => x.Key == "email")?.Value },
                { "subject", "Order confirmation" },
                { "orderId", orderIdString },
                { "orderDate", order.PlacedDate.ToString("dd/MM/yyyy") },
                { "companyName", orderCompany.Name },
                { "companyTheme", orderCompany.Color },
                { "companyLogo", orderCompany.Logo },
                { "orderList", orderListHTML },
            });
        }
    }
}