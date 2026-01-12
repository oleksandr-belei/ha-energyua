# Companion App Widget

<div align="center">
  <img width="151" height="100" hspace="15" alt="widget_template_scr1" src="https://github.com/user-attachments/assets/72bd7da5-7550-417c-b441-2c1a46cf0e49" />
  <img width="151" height="100" hspace="15" alt="widget_template_scr2" src="https://github.com/user-attachments/assets/8bb8f2ef-ebe3-4ccd-a75d-1c06f7a4cda4" />
  <img width="151" height="100" hspace="15" alt="widget_template_scr3" src="https://github.com/user-attachments/assets/b6487a71-3820-408c-97bd-d4a11aeddd37" />
</div>

This configuration creates a template sensor specifically designed for the **Home Assistant Companion App** on Android. It allows you to place a detailed, color-coded status card directly on your phone's home screen.

## Features:
* **State:** Provides a concise status (e.g., "💡 Включення о 18:00") suitable for simple State widgets.
* **Attribute (`html_card`):** Contains a detailed, color-coded HTML summary designed specifically for the **Template Widget**.

## YAML Configuration:
Add the following code to your `templates.yaml` file).

*Note: Replace `sensor.energyua_lvivska_grupa_1_1_...` with your actual entity IDs.*

```yaml
- sensor:
    - unique_id: energyua_widget
      name: "EnergyUA Widget"
      icon: mdi:flash-alert
      state: >
        {% set o_raw = states('sensor.energyua_lvivska_grupa_1_1_next_outage') %}
        {% set r_raw = states('sensor.energyua_lvivska_grupa_1_1_next_restore') %}
        
        {% if 'unavailable' in [o_raw, r_raw] %}
          ⚠️ Дані недоступні
        {% elif o_raw == 'unknown' and r_raw == 'unknown' %}
          ✅ Немає відключень
        {% else %}
          {% set o = o_raw | as_datetime | as_local if o_raw | as_datetime else None %}
          {% set r = r_raw | as_datetime | as_local if r_raw | as_datetime else None %}
          
          {% if r and not o %}
              💡 Відновлення о {{ r.strftime('%H:%M') }}
          {% elif o %}
              🕯️ Відключення о {{ o.strftime('%H:%M') }}
          {% endif %}
        {% endif %}
      
      attributes:
        html_card: >
          {% set o_raw = states('sensor.energyua_lvivska_grupa_1_1_next_outage') %}
          {% set r_raw = states('sensor.energyua_lvivska_grupa_1_1_next_restore') %}

          {% if 'unavailable' in [o_raw, r_raw] %}
            ⚠️ Дані недоступні
          {% elif o_raw == 'unknown' and r_raw == 'unknown' %}
            ✅ Немає запланованих відключень
          {% else %}
            {# Safe conversion to Local Time #}
            {% set o = o_raw | as_datetime | as_local if o_raw | as_datetime else None %}
            {% set r = r_raw | as_datetime | as_local if r_raw | as_datetime else None %}
            
            {# --- LOGIC: Determine Timer Mode --- #}
            {% set t = namespace(label='⏱️ Тривалість:', color='#03a9f4', sec=0) %}
            
            {% if o and r and o < r %}
                {% set t.sec = (r - o).total_seconds() %}
            {% elif o and o < r %}
                {% set t.label, t.color = '⏱️ До відключення:', '#ff9800' %}
                {% set t.sec = (o - now()).total_seconds() %}
            {% elif r %}
                {% set t.label, t.color = '⏱️ До відновлення:', '#ffc107' %}
                {% set t.sec = (r - now()).total_seconds() %}
            {% endif %}

            {# --- RENDER: HTML Output --- #}
            <p style="text-align:start">
              🕯️ Відключення: 
              {% if o %} <font color="#f44336"><b>{{ o.strftime('%H:%M') }}</b></font> <font color="#757575"><b>{{ o.strftime('%d.%m') }}</b></font>
              {% else %} <font color="#9e9e9e"><b>Невідомо</b></font> {% endif %}
              <br>
              💡 Відновлення: 
              {% if r %} <font color="#4caf50"><b>{{ r.strftime('%H:%M') }}</b></font> <font color="#757575"><b>{{ r.strftime('%d.%m') }}</b></font>
              {% else %} <font color="#9e9e9e"><b>Невідомо</b></font> {% endif %}
              <br>
              {{ t.label }} 
              {% if t.sec > 0 %}
                <font color="{{ t.color }}"><b>{{ (t.sec // 3600)|int }}:{{ '%02d'|format((t.sec % 3600)//60) }}</b></font>
              {% else %} — {% endif %}
            </p>
          {% endif %}
```
## Setup Widget
1. Add a **Home Assistant Template Widget** to your home screen.
2. In the widget settings, paste one of the following codes:

   **Option A: Full Status Card**
   ```yaml
   {{ state_attr('sensor.energyua_widget', 'html_card') }}
   ```

   **Option B: Simple Text Status**
   ```yaml
   {{ states('sensor.energyua_widget') }}
   ```
