using System;

namespace RMS.ViewModels.Products.Get
{
    public class ResponseViewModel
    {
        public int Id { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public string Image { get; set; }

        public float BasePrice { get; set; }
    }
}