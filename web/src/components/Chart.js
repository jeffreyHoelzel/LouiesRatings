import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis } from 'recharts';

const Chart = ({className, instructorName, searchBy}) => {
    const requestData = { class_name: className, instructor_name: instructorName, search_by: searchBy };
    const [data, setData] = useState([{grade: "empty", sum:0}]); // Initialize data that is graphed as empty

    useEffect(() => {
        const fetchData = async () => {
            const backendUrl = "/service/get_graph_data";

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
                    const chartData = JSON.parse(tempData);
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

export default Chart;