using System;

namespace RMS.ViewModels.Open_API.OpenProducts.GetAllProducts
{
    public class ResponseViewModel
    {
        public float BasePrice { get; set; }

        public string CompanyName { get; set; }
        
        public string Description { get; set; }

        public int Id { get; set; }

        public string Image { get; set; }

        public string Name { get; set; }
    }
}