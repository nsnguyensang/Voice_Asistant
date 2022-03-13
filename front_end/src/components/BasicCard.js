import { Card, CardContent, Typography } from '@mui/material'

function BasicCard({ user, content, color }) {
    return (
        <Card sx={{ minWidth: 275, mb: 2, border: 2, borderColor: color }}>
            <CardContent>
                <Typography sx={{ fontSize: 20}} color={color} gutterBottom>
                    {user}
                </Typography>
                <Typography sx={{ fontSize: 13 }} color="text.secondary" gutterBottom>
                    {content}
                </Typography>
            </CardContent>
      </Card>
    )
  }
  
  export default BasicCard