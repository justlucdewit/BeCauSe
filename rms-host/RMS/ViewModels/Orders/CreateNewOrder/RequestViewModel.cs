using System.Collections.Generic;
using RMS.Enums;

namespace RMS.ViewModels.Orders.CreateNewOrder
{
    public class RequestViewModel
    {
        public OrderStatus Status { get; set; }
        
        public Dictionary<string, string> CustomerDetails { get; set; }

        public List<OrderItemViewModel> OrderItems { get; set; }
    }
}