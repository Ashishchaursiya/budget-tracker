const renderchart = (data,labels,chart_type) =>{

    var ctx = document.getElementById('myChart').getContext('2d');
    
var myChart = new Chart(ctx, {
     
    type: chart_type,
    data: {
        labels: labels,
        datasets: [{
            label: 'last 6 month income',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title:{
            display:true,
            text:'income per category'
        },
        responsive: true,
         
        
    }
});
}
 
const getChartData = () =>{
    fetch("income-summary").then( (res) => res.json())
    .then( (result) => {
        console.log(result)
        const category_data=result.income_category;
        const [labels,data] = [Object.keys(category_data),Object.values(category_data)]
        var no = Math.floor(Math.random() * 5);
        var chart_show =['line','radar','bar','pie','doughnut'];
        renderchart(data,labels,chart_show[no]);
    });
}

document.onload =getChartData();