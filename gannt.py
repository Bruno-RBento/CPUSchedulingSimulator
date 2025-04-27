import plotly.graph_objects as go
import plotly.colors as pc
import plotly.io as pio
import tempfile


def gerar_grafico_png(processos):
    nomes_unicos = list({p['Processo'] for p in processos})
    paleta = pc.qualitative.Plotly
    while len(paleta) < len(nomes_unicos):
        paleta += paleta

    cores_por_processo = {
        nome: paleta[i] for i, nome in enumerate(sorted(nomes_unicos))
    }

    fig = go.Figure()

    adicionados = set()

    for p in processos:
        show_legend = p['Processo'] not in adicionados
        fig.add_trace(go.Bar(
            x=[p['Duracao']],
            y=["CPU"],
            base=p['Inicio'],
            name=p['Processo'],
            marker_color=cores_por_processo[p['Processo']],
            orientation='h',
            hovertemplate=f"{p['Processo']}: {p['Inicio']}s → {p['Inicio'] + p['Duracao']}s",
            showlegend=show_legend
        ))
        adicionados.add(p['Processo'])

    fig.update_layout(
        barmode='stack',
        title='Simulação de Escalonamento de Processos no CPU',
        xaxis=dict(
            title='Tempo (segundos)',
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        yaxis=dict(
            title='',
            showticklabels=False
        ),
        legend=dict(
            title='Processo',
            orientation='v',
            yanchor='top',
            y=1.0,
            xanchor='left',
            x=1.02,
            traceorder='normal',
            itemwidth=70,
            valign="top",
            borderwidth=0,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=10),
        ),
        height=400,
        width=900,
    )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    pio.write_image(fig, temp_file.name, format='png')
    return temp_file.name
