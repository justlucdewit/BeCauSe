using System;
using System.Collections.Generic;

namespace RMS.ViewModels.Orders
{
    public class OrderItemViewModel
    {
        public int ProductId { get; set; }
        
        public Dictionary<string, string> Settings { get; set; }
    }
}