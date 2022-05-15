using System;
using System.Collections.Generic;
using RMS.Models;

namespace RMS.ViewModels.Products.Update
{
    public class RequestViewModel
    {
        public int? Id { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public string Image { get; set; }

        public float BasePrice { get; set; }
        
        public List<ProductOptionsViewModel> ProductOptions { get; set; }
    }
}