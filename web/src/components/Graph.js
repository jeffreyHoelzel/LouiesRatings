import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis } from 'recharts';

const ChartComponent = () => {
    const [data, setData] = useState([{grade: "empty", sum:0}]); // Initialize data as empty

    useEffect(() => {
        const fetchData = async () => {
            const backendUrl = "/service/get_graph_data";

            // example data to request, use either class_name or instructor_name in search_by
            const requestData = { class_name: 'CS 386', instructor_name: 'Leverington,Michael E', search_by: "class_name" };

            try {
                // fetch data via class name
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
        
                if( response.ok ) {
                    // fill chart with fetched data
                    const tempData = await response.json();
                    const chartData = JSON.parse(tempData)
                    setData(chartData)
                }
                else {
                    throw new Error('Fetch was response unsuccessful');
                }

            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <BarChart width={450} height={300} data={data}>
            <Bar dataKey="sum" fill="#002454" />
            <XAxis dataKey="grade" />
            <YAxis />
        </BarChart>
    );
};

export default ChartComponent;