import pandas as pd
from pathlib import Path
import folium
from folium.plugins import MarkerCluster
from folium.plugins import Search
from branca.element import Template, MacroElement

def create_cluster_icon(color):
    return f"""
    function(cluster) {{
        return L.divIcon({{
            html: `
                <div style="
                    background-color: {color};
                    border-radius: 50%;
                    box-shadow: 0 0 6px 3px rgba(0, 0, 0, 0);
                    width: 30px;
                    height: 30px;
                    line-height: 30px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    border: 1.5px solid rgba(0, 0, 0, 0);
                    overflow: visible;
                ">
                    <span>` + cluster.getChildCount() + `</span>
                </div>
            `,
            className: 'marker-cluster',
            iconSize: new L.Point(40, 40)
        }});
    }}
    """

def shutdown(shutdown_df):
    group = folium.FeatureGroup(name="Shutdown", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("red"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    shutdown_df.fillna("Not Available", inplace=True)
    for _, row in shutdown_df.iterrows():
        shutdown_str = (
                f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
                f"<b>Status:</b> Shutdown<br>"
                f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
                f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
                f"<b>Operational from:</b> {row['OperationalFrom']}<br>"
                f"<b>Operational to:</b> {row['OperationalTo']}<br>"
                f"<b>Construction started at:</b> {row['ConstructionStartAt']}<br>"
                f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
                f"<b>IAEAId:</b> {int(row['IAEAId'])}<br>"
                f"<b>Source:</b> {row['Source']}<br>"
            )        
        shutdown_popup_html = folium.Popup(folium.Html(shutdown_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=shutdown_popup_html,
            icon=folium.Icon(icon="remove", color="red"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def operational(operational_df):
    group = folium.FeatureGroup(name="Operational", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("green"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    ) 
    operational_df = operational_df.drop(['OperationalFrom','OperationalTo'], axis=1)   
    operational_df.fillna("Not Available", inplace=True)
    for _, row in operational_df.iterrows():
        operational_str =(
                f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
                f"<b>Status:</b> Operational<br>"
                f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
                f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
                f"<b>Construction started at:</b> {row['ConstructionStartAt']}<br>"
                f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
                f"<b>IAEAId:</b> {int(row['IAEAId'])}<br>"
                f"<b>Source:</b> {row['Source']}<br>"
            )       
        operational_popup_html = folium.Popup(folium.Html(operational_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=operational_popup_html,
            icon=folium.Icon(icon="ok", color="green"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def cancelled_construction(cancelled_construction_df):
    group = folium.FeatureGroup(name="Cancelled Construction", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("orange"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    ) 
    cancelled_construction_df = cancelled_construction_df.drop(['ReactorModel','ConstructionStartAt','OperationalFrom','OperationalTo'], axis=1)    
    for _, row in cancelled_construction_df.iterrows():
        cancelled_construction_str =(
                f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
                f"<b>Status:</b> Cancelled Construction<br>"
                f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
                f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
                f"<b>Source:</b> {row['Source']}<br>"
            )       
        cancelled_construction_popup_html = folium.Popup(folium.Html(cancelled_construction_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=cancelled_construction_popup_html,
            icon=folium.Icon(icon="remove", color="orange"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def under_construction(under_construction_df):
    group = folium.FeatureGroup(name="Under Construction", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("orange"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    under_construction_df = under_construction_df.dropna(subset=["Latitude", "Longitude"])
    under_construction_df = under_construction_df.drop(['IAEAId','OperationalFrom','OperationalTo'], axis=1)    
    under_construction_df.fillna("Not Available", inplace=True)
    for _, row in under_construction_df.iterrows():
        under_construction_str =(
            f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
            f"<b>Status:</b> Under construction<br>"
            f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
            f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
            f"<b>Construction started at:</b> {row['ConstructionStartAt']}<br>"
            f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
            f"<b>Source:</b> {row['Source']}<br>"
        )      
        under_construction_popup_html = folium.Popup(folium.Html(under_construction_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=under_construction_popup_html,
            icon=folium.Icon(icon="wrench", color="orange"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def planned(planned_df):
    group = folium.FeatureGroup(name="Planned", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("blue"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    planned_df = planned_df.drop(['IAEAId','Capacity','ConstructionStartAt','OperationalFrom','OperationalTo'], axis=1)    
    planned_df.fillna("Not Available", inplace=True)
    for _, row in planned_df.iterrows():
        planned_str =(
            f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
            f"<b>Status:</b> Planned<br>"
            f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
            f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
            f"<b>Source:</b> {row['Source']}<br>"
        )      
        planned_popup_html = folium.Popup(folium.Html(planned_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=planned_popup_html,
            icon=folium.Icon(icon="time", color="blue"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def suspended_operation(suspended_operation_df):
    group = folium.FeatureGroup(name="Suspended Operation", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("darkred"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    suspended_operation_df = suspended_operation_df.drop(['OperationalTo'], axis=1)    
    suspended_operation_df.fillna("Not Available", inplace=True)
    for _, row in suspended_operation_df.iterrows():
        suspended_operation_str =(
            f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
            f"<b>Status:</b> Suspended Operation<br>"
            f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
            f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
            f"<b>Operational from:</b> {row['OperationalFrom']}<br>"
            f"<b>Construction started at:</b> {row['ConstructionStartAt']}<br>"
            f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
            f"<b>IAEAId:</b> {int(row['IAEAId'])}<br>"
            f"<b>Source:</b> {row['Source']}<br>"
        )        
        suspended_operation_popup_html = folium.Popup(folium.Html(suspended_operation_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=suspended_operation_popup_html,
            icon=folium.Icon(icon="pause", color="darkred"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def suspended_construction(suspended_construction_df):
    group = folium.FeatureGroup(name="Suspended Construction", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("orange"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    suspended_construction_df = suspended_construction_df.drop(['OperationalFrom','OperationalTo','IAEAId'], axis=1)   
    suspended_construction_df.fillna("Not Available", inplace=True)
    for _, row in suspended_construction_df.iterrows():
        suspended_construction_str =(
            f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
            f"<b>Status:</b> Suspended Construction<br>"
            f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
            f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
            f"<b>Construction started at:</b> {row['ConstructionStartAt']}<br>"
            f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
            f"<b>Source:</b> {row['Source']}<br>"
            )        
        suspended_construction_popup_html = folium.Popup(folium.Html(suspended_construction_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=suspended_construction_popup_html,
            icon=folium.Icon(icon="pause", color="orange"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def never_comm(never_comm_df):
    group = folium.FeatureGroup(name="Never Commissioned", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("gray"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    never_comm_df = never_comm_df.drop(['IAEAId','ConstructionStartAt','OperationalFrom','OperationalTo'], axis=1)    
    never_comm_df.fillna("Not Available", inplace=True)
    for _, row in never_comm_df.iterrows():
        never_comm_str =(
            f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
            f"<b>Status:</b> Never Commissioned<br>"
            f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
            f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
            f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
            f"<b>Source:</b> {row['Source']}<br>"
        )        
        never_comm_popup_html = folium.Popup(folium.Html(never_comm_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=never_comm_popup_html,
            icon=folium.Icon(icon="remove-sign", color="gray"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster)
    return group

def decomm_completed(decomm_completed_df):
    group = folium.FeatureGroup(name="Decommissioning Completed", show=True)
    marker_cluster = MarkerCluster(
        icon_create_function=create_cluster_icon("red"),
        maxClusterRadius=5,
        spiderfyOnMaxZoom=True,
    )
    decomm_completed_df = decomm_completed_df.drop(['OperationalFrom'], axis=1)    
    decomm_completed_df.fillna("Not Available", inplace=True)
    for _, row in decomm_completed_df.iterrows():
        decomm_completed_str =(
            f"<div style='text-align:center;'><b>{row['Name']}</b></div>"
            f"<b>Status:</b> Decommissioning Completed<br>"
            f"<b>Reactor Type:</b> {row['ReactorType']}<br>"
            f"<b>Reactor Model:</b> {row['ReactorModel']}<br>"
            f"<b>Operational to:</b> {row['OperationalTo']}<br>"
            f"<b>Construction started at:</b> {row['ConstructionStartAt']}<br>"
            f"<b>Capacity:</b> {row['Capacity']} MWe<br>"
            f"<b>IAEAId:</b> {int(row['IAEAId'])}<br>"
            f"<b>Source:</b> {row['Source']}<br>"
        )     
        decomm_completed_popup_html = folium.Popup(folium.Html(decomm_completed_str, script=True), max_width=300)
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['Name'],
            popup=decomm_completed_popup_html,
            icon=folium.Icon(icon="check", color="red"),
        )
        marker_cluster.add_child(marker)
    group.add_child(marker_cluster) 
    return group

def addtogroup(df,group):
    for _, row in df.iterrows():
        marker = folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            name = row['Name'],
            icon=folium.DivIcon(html=''),
        ).add_to(group)
    
def make_map(df):
    df['Status'] = df['Status'].str.strip().str.title().str.replace(" ", "").str.lower()
    loc_avg = df['Latitude'].mean(),df['Longitude'].mean()
    
    m = folium.Map(
        location=loc_avg,
        zoom_start=3,
        max_bounds=True,
        no_wrap=True,
        tiles=None 
    )

    attr = (
        '&copy; <a href="https://github.com/cristianst85/GeoNuclearData?tab=License-1-ov-file">GeoNuclearData</a> (ODbL), '
        '&copy; <a href="https://carto.com/attributions">CARTO</a>, '
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    )
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
        attr=attr,
        name='Carto Voyager',
        min_zoom=3,
        max_zoom=18,
    ).add_to(m)

    df = df.drop(['Country','CountryCode','LastUpdatedAt',], axis=1)
    df = df.dropna(subset=["Latitude", "Longitude"])    

    shutdown_df = df[df['Status'] == 'shutdown'].copy()
    under_construction_df = df[df['Status'] == 'underconstruction'].copy()
    operational_df = df[df['Status'] == 'operational'].copy()
    cancelled_construction_df = df[df['Status'] == 'cancelledconstruction'].copy()
    planned_df = df[df['Status'] == 'planned'].copy()
    suspended_operation_df = df[df['Status'] == 'suspendedoperation'].copy()
    suspended_construction_df = df[df['Status'] == 'suspendedconstruction'].copy()
    never_comm_df = df[df['Status'] == 'nevercommissioned'].copy()
    decomm_completed_df = df[df['Status'] == 'decommissioningcompleted'].copy()

    operational_grp = operational(operational_df)    
    shutdown_grp = shutdown(shutdown_df)
    cancelled_construction_grp = cancelled_construction(cancelled_construction_df)
    under_construction_grp = under_construction(under_construction_df)
    planned_grp = planned(planned_df)
    suspended_operation_grp = suspended_operation(suspended_operation_df)
    suspended_construction_grp = suspended_construction(suspended_construction_df)
    never_comm_grp = never_comm(never_comm_df)
    decomm_completed_grp = decomm_completed(decomm_completed_df)

    operational_grp.add_to(m)
    shutdown_grp.add_to(m)
    cancelled_construction_grp.add_to(m)
    under_construction_grp.add_to(m)
    planned_grp.add_to(m)
    suspended_operation_grp.add_to(m)
    suspended_construction_grp.add_to(m)
    never_comm_grp.add_to(m)
    decomm_completed_grp.add_to(m)

    search_group = folium.FeatureGroup(
        control=False,
        show=False
    ).add_to(m)

    addtogroup(operational_df,search_group)
    addtogroup(shutdown_df,search_group)
    addtogroup(cancelled_construction_df,search_group)
    addtogroup(under_construction_df,search_group)
    addtogroup(planned_df,search_group)
    addtogroup(suspended_operation_df,search_group)
    addtogroup(suspended_construction_df,search_group)
    addtogroup(never_comm_df,search_group)
    addtogroup(decomm_completed_df,search_group)

    search = Search(
        layer=search_group,
        placeholder="Search for a Nuclear Reactor",
        collapsed=True,
        search_label="name",
    ).add_to(m)

    operational_amount = len(operational_df)
    shutdown_amount = len(shutdown_df)
    cancelled_construction_amount = len(cancelled_construction_df)
    under_construction_amount = len(under_construction_df)
    planned_amount = len(planned_df)
    suspended_operation_amount = len(suspended_operation_df)
    suspended_construction_amount = len(suspended_construction_df)
    never_comm_amount = len(never_comm_df)
    decomm_completed_amount = len(decomm_completed_df)

    stats_html = f"""
    <div id="plant-status-summary" style="position: absolute; left: 20px; bottom: 20px; background-color: #fff;
        padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); font-family: Arial, sans-serif; max-width: 400px; z-index: 9999;">
        <h1 style="font-size: 20px; margin-bottom: 20px; cursor: pointer;" onclick="toggleSummary()">
            Plant Status Summary &#x25BC;
        </h1>
        <div id="summary-content">
            <p><strong>Operational:</strong> {operational_amount}</p>
            <p><strong>Shut down:</strong> {shutdown_amount}</p>
            <p><strong>Cancelled Construction:</strong> {cancelled_construction_amount}</p>
            <p><strong>Under Construction:</strong> {under_construction_amount}</p>
            <p><strong>Planned:</strong> {planned_amount}</p>
            <p><strong>Suspended Operation:</strong> {suspended_operation_amount}</p>
            <p><strong>Suspended Construction:</strong> {suspended_construction_amount}</p>
            <p><strong>Never Commissioned:</strong> {never_comm_amount}</p>
            <p><strong>Decommissioning Completed:</strong> {decomm_completed_amount}</p>
        </div>
    </div>
    """
    script_html = """
    <script>
    function toggleSummary() {
        var content = document.getElementById("summary-content");
        var header = document.querySelector("#plant-status-summary h1");
        if (content.style.display === "none") {
            content.style.display = "block";
            header.innerHTML = "Plant Status Summary &#x25BC;";
        } else {
            content.style.display = "none";
            header.innerHTML = "Plant Status Summary &#x25B2;";
        }
    }
    </script>
    """
    macro_html= f"""
            {{% macro html(this, kwargs) %}}
            {stats_html}
            {script_html}
            {{% endmacro %}}
        """

    macro = MacroElement()
    macro._template = Template(macro_html)
    m.get_root().add_child(macro)

    folium.LayerControl(collapsed=True).add_to(m)
    return m

def main():
    file = Path(__file__).parent / "nuclear_power_plants.csv"

    df = pd.read_csv(file)

    m = make_map(df)

    file = Path(__file__).parent / "docs" / "index.html"
    
    m.save(str(file))

if __name__ == '__main__':
    main()